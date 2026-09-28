# 🧠 KernelSense - AI Operating-System Assistant

KernelSense is an intelligent AI assistant that lets you interact with your operating system using natural language. No more memorizing complex commands—just ask in plain English!

## 🌟 What is KernelSense?

Operating systems contain many powerful tools, but users often need technical knowledge to use them effectively. KernelSense bridges this gap by allowing you to:

- **Diagnose system issues** in natural language
- **Monitor system resources** (CPU, RAM, disk, network)
- **Manage processes** safely
- **Find and manage files** easily
- **Get explanations** instead of raw command output

Instead of learning commands, just ask:

- "Why is my computer slow?"
- "Which process is using the most RAM?"
- "Find all Python files"

## ✨ Key Features

### 🔍 System Diagnostics

- Automatic slowness diagnosis
- CPU, memory, disk, and network monitoring
- Process analysis and recommendations
- System overview and health checks

### 🛡️ Built-in Security

- **Risk Assessment**: Every operation is analyzed for potential impact
- **User Approval**: Dangerous operations require explicit confirmation
- **Safety Warnings**: Clear explanations of consequences before execution
- **Protected Processes**: Critical system processes are specially protected

### 📝 Comprehensive Audit Logging

- All operations are logged with timestamps
- Tracks user decisions (approved/denied)
- JSON and text log formats
- Session statistics and history

### 🎯 Natural Language Understanding

- No commands to memorize
- Understands variations in phrasing
- Extracts parameters automatically
- Helpful error messages

## 📋 Requirements

- **Python 3.7+**
- **Windows** (primary support), Linux/Mac (partial support)
- Administrator privileges (for some operations)

## 🚀 Installation

1. **Clone or download the project**

```bash
cd KernelSense
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run KernelSense**

```bash
python kernelsense.py
```

## 💡 Usage Examples

### System Diagnostics

```md
You: Why is my computer slow?
KernelSense: Analyzes CPU, RAM, disk, and running processes...

You: Show CPU usage
KernelSense: Displays current CPU utilization and per-core breakdown

You: Check RAM
KernelSense: Shows memory usage, available RAM, and swap status

You: Check disk space
KernelSense: Lists all drives with usage percentages
```

### Process Management

```md
You: List processes
KernelSense: Shows top 10 processes by memory usage

You: Show top processes by CPU
KernelSense: Lists CPU-intensive processes

You: Show info for process 1234
KernelSense: Displays detailed information about that process

You: Kill process 5678
⚠️ HIGH RISK operation
KernelSense: Requests approval before stopping the process
```

### File Operations

```sh
You: Find Python files
KernelSense: Searches recursively and lists .py files

You: Find files named config.txt
KernelSense: Locates files matching that name
```

### Getting Help

```sh
You: help
KernelSense: Shows all available commands and examples

You: exit
KernelSense: Displays session summary and exits
```

## 🔒 Security Model

KernelSense implements a multi-layered security approach:

### Risk Levels

1. **SAFE** - Read-only operations (show CPU, list processes)
2. **LOW** - Minimal system interaction (find files)
3. **MEDIUM** - System changes possible
4. **HIGH** - Significant system changes (kill process)
5. **CRITICAL** - Destructive operations (delete files)

### Approval Flow

```ini
User Request
    ↓
Intent Parsing
    ↓
Risk Assessment
    ↓
Requires Approval? → YES → Display Warning → Get User Confirmation
    ↓                                              ↓
    NO                                         Approved?
    ↓                                              ↓
Execute Operation  ← ← ← ← ← ← ← ← ← ← ← ← ← ← YES
    ↓
Log Result
```

### Protected Processes

Critical system processes are specially protected:

- `system`, `csrss.exe`, `lsass.exe`, `explorer.exe` (Windows)
- `systemd`, `init`, `kernel` (Linux)
- Extra warnings before attempting to stop these

## 📊 Audit Logging

All operations are logged to the `logs/` directory:

### Log Files

- `kernelsense_YYYYMMDD.log` - Human-readable text log
- `kernelsense_YYYYMMDD.json` - Structured JSON log

### Log Contents

- Timestamp of operation
- User intent and parameters
- Success/failure status
- Risk level
- Approval decisions
- Error messages

### Viewing Logs

Logs are automatically created in the `logs/` directory and can be reviewed for:

- Security auditing
- Troubleshooting
- Usage analysis
- Compliance tracking

## 🏗️ Architecture

```ini
kernelsense.py (Entry Point)
    ↓
cli/interface.py (User Interface)
    ↓
├── core/intent_parser.py (Natural Language Understanding)
├── core/command_router.py (Command Routing)
├── core/operations.py (System Operations)
├── security/validator.py (Security Checks)
├── security/approval_manager.py (User Approvals)
├── system_info/collector.py (System Information)
└── core/audit_logger.py (Logging)
```

### Module Overview

- **cli/** - Command-line interface with colored output
- **core/** - Intent parsing, routing, operations, logging
- **security/** - Risk assessment, validation, approvals
- __system_info/__ - System monitoring and data collection
- **logs/** - Audit logs (created automatically)

## 🛠️ Extending KernelSense

### Adding New Commands

1. __Add Intent__ to `core/intent_parser.py`:

```python
Intent.NEW_COMMAND = "new_command"
```

2. **Add Pattern** to recognize the command:

```python
Intent.NEW_COMMAND: [
    r'\b(pattern|to|match)\b',
]
```

3. __Add Handler__ in `core/command_router.py`:

```python
def _handle_new_command(self, params):
    # Implementation
    return result
```

4. __Set Risk Level__ in `security/risk_assessor.py`:

```python
Intent.NEW_COMMAND: RiskLevel.SAFE,
```

## 📝 Examples of Natural Language Queries

KernelSense understands variations:

**System Performance:**

- "Why is my computer running slow?"
- "What's making my PC sluggish?"
- "Diagnose performance issues"
- "Check system performance"

**CPU Monitoring:**

- "Show CPU usage"
- "What's my processor usage?"
- "Check CPU"
- "How much CPU am I using?"

**Memory:**

- "Check RAM"
- "How much memory is available?"
- "Show memory usage"

**Processes:**

- "List running processes"
- "What processes are running?"
- "Show me active applications"
- "Which app is using the most memory?"

## ⚠️ Important Notes

### Administrator Privileges

Some operations may require administrator/root privileges:

- Stopping certain processes
- Accessing system directories
- Viewing all processes

### Windows-Specific Features

- Startup applications detection works best on Windows
- Process management is optimized for Windows

### Safety

- **Always read warnings carefully** before approving operations
- **Backup important data** before file operations
- **Review audit logs** regularly
- **Test in safe environments** first

## 🐛 Troubleshooting

### "Access Denied" Errors

- Run as Administrator (Windows) or with sudo (Linux/Mac)
- Check file/process permissions

### "Process Not Found"

- Process may have already terminated
- Verify PID is correct
- Use "list processes" to see available processes

### Dependencies Not Installed

```bash
pip install -r requirements.txt
```

### Colorama Not Working

Colorama is automatically initialized on Windows. If colors don't display:

```bash
pip install --upgrade colorama
```

## 📄 License

This project is created for educational purposes as part of an Operating Systems course project.

## 👥 Contributing

Contributions are welcome! Areas for improvement:

- Support for more operating systems
- Additional system operations
- Enhanced natural language understanding
- UI improvements
- Performance optimizations

## 🔮 Future Enhancements

- [ ] Web-based interface
- [ ] Remote system monitoring
- [ ] Scheduled operations
- [ ] Machine learning for better intent recognition
- [ ] Plugin system for custom commands
- [ ] Multi-language support
- [ ] Voice input support

## 📞 Support

For issues or questions:

1. Check the troubleshooting section
2. Review audit logs for error messages
3. Use the `help` command for examples

---

**Remember:** KernelSense is a powerful tool. Always read warnings carefully and understand what operations will do before approving them!

🧠 **Happy System Managing!**
