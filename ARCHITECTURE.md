# KernelSense Architecture Documentation

## Overview

KernelSense is built with a modular architecture that separates concerns into distinct layers: interface, processing, security, operations, and logging.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
└──────────────────────────┬──────────────────────────────────┘
                           │ Natural Language Input
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    CLI Layer (cli/)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │   interface.py - User Interface & Session Management │  │
│  │   - Input/Output handling                            │  │
│  │   - Colored display with colorama                    │  │
│  │   - Session statistics                               │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                 Core Processing Layer (core/)                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  intent_parser.py - Natural Language Understanding    │  │
│  │  - Regex pattern matching                            │  │
│  │  - Parameter extraction                              │  │
│  │  - Intent classification                             │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │                                  │
│                           ↓                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  command_router.py - Request Routing                 │  │
│  │  - Maps intents to handlers                          │  │
│  │  - Orchestrates execution flow                       │  │
│  └────────────────────────┬─────────────────────────────┘  │
└───────────────────────────┼──────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Security   │   │   System     │   │   Audit      │
│   Layer      │   │   Info       │   │   Logging    │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        ↓                   ↓                   ↓
┌──────────────────────────────────────────────────────┐
│  security/               system_info/    core/       │
│  - risk_assessor.py     - collector.py  audit_logger│
│  - validator.py         - formatters.py             │
│  - approval_manager.py                               │
└────────────────────────┬─────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              Operations Layer (core/operations.py)           │
│  - Process management (kill, list, info)                    │
│  - File operations (find, delete, search)                   │
│  - System queries (startup apps, services)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    Operating System                          │
│  - Windows/Linux/Mac APIs                                   │
│  - psutil library (cross-platform)                          │
└─────────────────────────────────────────────────────────────┘
```

## Layer Descriptions

### 1. CLI Layer (`cli/`)

**Purpose:** User interaction and presentation

**Components:**
- `interface.py`: Main CLI class
  - Manages the input/output loop
  - Coordinates all other components
  - Displays colored output
  - Shows session statistics

**Responsibilities:**
- Accept user input
- Display results with appropriate formatting
- Handle keyboard interrupts
- Show session summaries

### 2. Core Processing Layer (`core/`)

**Purpose:** Understanding and routing user requests

**Components:**

#### `intent_parser.py`
- **Intent Enum**: Defines all possible user intents
- **IntentParser Class**: 
  - Pattern matching using regex
  - Parameter extraction from natural language
  - Confidence scoring
  - Help text generation

**Intent Categories:**
- System diagnostics (CPU, memory, disk, network)
- Process management (list, find, kill, info)
- File operations (find, delete, search)
- System operations (startup apps, services)
- Utility (help, exit)

#### `command_router.py`
- **CommandRouter Class**:
  - Maps intents to handler methods
  - Invokes appropriate handlers
  - Returns standardized response format

**Response Format:**
```python
{
    'success': bool,
    'message': str,
    'data': Any,
    'requires_approval': bool
}
```

#### `operations.py`
- **SystemOperations Class**:
  - Implements actual system operations
  - Process management
  - File system operations
  - Returns success/error information

### 3. Security Layer (`security/`)

**Purpose:** Risk assessment and user protection

**Components:**

#### `risk_assessor.py`
- **RiskLevel Enum**: SAFE, LOW, MEDIUM, HIGH, CRITICAL
- **RiskAssessor Class**:
  - Assesses operation risk
  - Identifies critical processes
  - Determines consequences
  - Validates operations

**Risk Decision Tree:**
```
Operation Request
    ↓
Base Risk Level (by intent type)
    ↓
Parameter Analysis
    ↓
Risk Adjustment
    ↓
    ├── SAFE/LOW → Auto-approve
    └── HIGH/CRITICAL → Require approval
```

#### `validator.py`
- **SecurityValidator Class**:
  - Validates operation parameters
  - Combines risk assessment
  - Generates approval prompts
  - Checks permissions

#### `approval_manager.py`
- **ApprovalManager Class**:
  - Records approval requests
  - Tracks decisions
  - Maintains history
  - Provides statistics

- **ApprovalPrompt Class**:
  - Interactive user prompts
  - Validates user responses
  - Handles confirmation flow

### 4. System Information Layer (`system_info/`)

**Purpose:** Collect and format system data

**Components:**

#### `collector.py`
- **SystemInfoCollector Class**:
  - Uses `psutil` for cross-platform access
  - Collects CPU, memory, disk, network data
  - Lists and analyzes processes
  - Diagnoses system issues

**Methods:**
- `get_cpu_info()`: CPU usage and specs
- `get_memory_info()`: RAM and swap usage
- `get_disk_info()`: Disk space per partition
- `get_process_list()`: Running processes
- `get_network_info()`: Network statistics
- `diagnose_slowness()`: Automatic diagnosis

#### `formatters.py`
- **SystemInfoFormatter Class**:
  - Converts raw data to human-readable strings
  - Adds visual indicators (✓, ⚠️, 🔴)
  - Formats tables and lists
  - Truncates long output

### 5. Audit Logging Layer (`core/audit_logger.py`)

**Purpose:** Comprehensive operation logging

**Components:**

#### `audit_logger.py`
- **AuditLogger Class**:
  - Dual logging (text + JSON)
  - Session tracking
  - Statistics generation
  - Log export functionality

**Log Information:**
- Timestamp
- User intent and parameters
- Success/failure status
- Risk level
- Approval decisions
- Results or error messages

**Log Files:**
- `logs/kernelsense_YYYYMMDD.log` (text)
- `logs/kernelsense_YYYYMMDD.json` (structured)

## Data Flow

### Example: "Why is my computer slow?"

```
1. User Input: "Why is my computer slow?"
        ↓
2. CLI captures input → logs to audit
        ↓
3. IntentParser analyzes:
   - Pattern match: "slow" → Intent.DIAGNOSE_SLOWNESS
   - Confidence: 0.85
   - Parameters: {}
        ↓
4. SecurityValidator checks:
   - Intent: DIAGNOSE_SLOWNESS
   - Risk Level: SAFE
   - Requires approval: False
        ↓
5. CommandRouter routes to handler:
   - _handle_diagnose_slowness()
        ↓
6. SystemInfoCollector gathers data:
   - CPU usage
   - Memory usage
   - Running processes
   - Disk usage
        ↓
7. Diagnosis analysis:
   - Identifies issues
   - Determines severity
        ↓
8. SystemInfoFormatter formats output:
   - Human-readable messages
   - Color coding
   - Visual indicators
        ↓
9. CLI displays result
        ↓
10. AuditLogger records operation:
    - Intent, success, data
```

### Example: "Kill process 1234" (with approval)

```
1. User Input: "Kill process 1234"
        ↓
2. IntentParser:
   - Intent: KILL_PROCESS
   - Parameters: {pid: 1234}
        ↓
3. SecurityValidator:
   - Risk Level: HIGH
   - Requires approval: True
   - Checks if process is critical
        ↓
4. ApprovalPrompt displays:
   - Risk warning
   - Consequences
   - Request confirmation
        ↓
5. User responds: "yes" or "no"
        ↓
6. If approved:
   ├─→ SystemOperations.kill_process_by_pid(1234)
   ├─→ AuditLogger logs (approved=True)
   └─→ CLI displays result
   
   If denied:
   ├─→ Operation cancelled
   ├─→ AuditLogger logs (approved=False)
   └─→ CLI shows cancellation message
```

## Design Patterns

### 1. Strategy Pattern
- Multiple risk levels with different handling strategies
- Different formatters for different data types

### 2. Command Pattern
- Intents represent commands
- Router dispatches to appropriate handlers

### 3. Chain of Responsibility
- Request flows through validation → approval → execution
- Each step can pass or block the request

### 4. Observer Pattern
- Audit logger observes all operations
- Records every significant event

### 5. Factory Pattern
- IntentParser creates appropriate Intent objects
- Risk assessor creates risk assessment objects

## Extension Points

### Adding New Commands

1. **Define Intent** in `intent_parser.py`
2. **Add Patterns** for recognition
3. **Create Handler** in `command_router.py`
4. **Set Risk Level** in `risk_assessor.py`
5. **Implement Operation** in `operations.py` (if needed)

### Adding New Data Sources

1. **Create Collector Method** in `system_info/collector.py`
2. **Create Formatter** in `system_info/formatters.py`
3. **Add Handler** in `command_router.py`

### Custom Risk Policies

1. **Modify Risk Levels** in `risk_assessor.py`
2. **Adjust Approval Logic** in `validator.py`
3. **Customize Prompts** in `approval_manager.py`

## Testing Considerations

### Unit Testing
- Test intent parsing with various inputs
- Test risk assessment logic
- Test formatters with edge cases

### Integration Testing
- Test full flow from input to output
- Test approval workflow
- Test error handling

### Security Testing
- Verify all high-risk operations require approval
- Test with critical system processes
- Verify audit logging completeness

## Performance Considerations

### Optimization Points
- System info caching (configurable)
- Limit process list size
- Limit file search depth
- Async operations (future enhancement)

### Resource Management
- Process iteration is memory-efficient
- File search has configurable limits
- Logs are rotated daily

## Security Considerations

### Defense in Depth
1. **Input Validation**: Regex patterns validate intent
2. **Risk Assessment**: Every operation is evaluated
3. **User Approval**: High-risk operations require confirmation
4. **Audit Logging**: All operations are recorded
5. **Process Protection**: Critical processes have extra warnings

### Privilege Management
- Operations run with user's privileges
- No privilege escalation attempts
- Clear error messages for permission issues

## Configuration

See `config.py` for customizable settings:
- Process limits
- File search limits
- Risk thresholds
- Logging options
- Feature flags

---

This architecture provides a robust, secure, and extensible foundation for KernelSense!
