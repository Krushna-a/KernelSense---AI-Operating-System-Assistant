# KernelSense Usage Examples

This document provides detailed examples of using KernelSense for common tasks.

## 🔍 System Diagnostics

### Example 1: Diagnosing Slowness

**Scenario:** Your computer is running slowly and you want to find out why.

```
You: Why is my computer slow?

KernelSense: 
System Status: WARNING

Issues Found:
🟠 [MEMORY] RAM usage is very high (87.3%). Using 14.2 GB of 16.0 GB
🟡 [PROCESS] Process 'chrome.exe' (PID 5432) is using 2847 MB of memory
```

**What it does:**
- Checks CPU usage
- Analyzes RAM consumption
- Identifies memory-hungry processes
- Checks disk usage
- Looks for system errors

### Example 2: Detailed CPU Check

```
You: Show CPU usage

KernelSense:
CPU Usage: 23.5% [NORMAL]
CPU Cores: 8 (4 physical)
Frequency: 2400.00 MHz
```

### Example 3: Memory Analysis

```
You: Check RAM

KernelSense:
RAM: 7.82 GB / 16.0 GB (48.8%) [NORMAL]
Available: 8.18 GB
Swap: 0.5 GB / 4.0 GB (12.5%)
```

## 📊 Process Management

### Example 4: Listing Processes

```
You: List processes

KernelSense:
Top 10 processes by memory:

PID      Name                          CPU %    Memory MB    Memory %   Status    
------------------------------------------------------------------------------------------
5432     chrome.exe                    12.3     2847.32      17.80      running   
8765     python.exe                    45.1     1256.78      7.86       running   
2341     Code.exe                      8.9      982.45       6.14       running   
```

### Example 5: Finding CPU-Intensive Processes

```
You: Show top processes by CPU

KernelSense:
Top 10 processes by cpu:

PID      Name                          CPU %    Memory MB    Memory %   Status    
------------------------------------------------------------------------------------------
8765     python.exe                    45.1     1256.78      7.86       running   
5432     chrome.exe                    12.3     2847.32      17.80      running   
```

### Example 6: Process Details

```
You: Show info for process 5432

KernelSense:
Process Information:
  PID: 5432
  Name: chrome.exe
  Status: running
  Username: DESKTOP\User
  Created: 2026-09-28 10:15:43
  CPU Usage: 12.3%
  Memory: 2847.32 MB (17.8%)
  Threads: 42
  Working Directory: C:\Program Files\Google\Chrome\Application
  Executable: C:\Program Files\Google\Chrome\Application\chrome.exe
```

### Example 7: Stopping a Process (with Approval)

```
You: Kill process 8765

KernelSense:
============================================================
⚠️ HIGH RISK - significant system changes
============================================================

Operation: Stop process with PID 8765

Stopping this process may cause data loss or application crashes.

Potential consequences:
  • Application will close immediately
  • Unsaved work will be lost
  • Related processes may be affected

============================================================

Do you want to proceed? (yes/no): yes

⚙️  Processing...

✓ Process 'python.exe' (PID 8765) has been stopped.
```

### Example 8: Stopping a Critical Process

```
You: Kill process named explorer.exe

KernelSense:
============================================================
🔴 CRITICAL RISK - destructive operation
============================================================

Operation: Stop process named 'explorer.exe'

⚠️ 'explorer.exe' is a critical system process!

Potential consequences:
  • System may become unstable
  • You may lose unsaved work
  • System restart may be required
  • Windows/System may crash

============================================================

Do you want to proceed? (yes/no): no

Operation cancelled by user.
```

## 📁 File Operations

### Example 9: Finding Files by Type

```
You: Find Python files

KernelSense:
Found 15 file(s):

  • main.py (0.05 MB)
    C:\Code\Projects\myapp\main.py
  • config.py (0.01 MB)
    C:\Code\Projects\myapp\config.py
  • utils.py (0.03 MB)
    C:\Code\Projects\myapp\utils.py
  
  ... and 12 more files
```

### Example 10: Finding Specific Files

```
You: Find files named "test.txt"

KernelSense:
Found 3 file(s):

  • test.txt (0.02 MB)
    C:\Users\User\Documents\test.txt
  • test.txt (0.01 MB)
    C:\Temp\test.txt
  • test.txt (0.00 MB)
    C:\Code\test.txt
```

## 💾 Disk Monitoring

### Example 11: Checking Disk Space

```
You: Show disk space

KernelSense:
✓ C:\ (NTFS): 234.56 GB / 476.93 GB (49% used, 242.37 GB free)
⚠️ D:\ (NTFS): 18.23 GB / 19.53 GB (93% used, 1.3 GB free)
```

## 🌐 Network Information

### Example 12: Network Statistics

```
You: Check network

KernelSense:
Sent: 1247.82 MB (523847 packets)
Received: 3421.56 MB (892341 packets)
Active Connections: 47
```

## 📋 System Overview

### Example 13: Complete System Information

```
You: System overview

KernelSense:
Platform: Windows 11
Architecture: AMD64
Hostname: DESKTOP-ABC123
Processor: Intel(R) Core(TM) i7-9700K CPU @ 3.60GHz
Boot Time: 2026-09-28 08:30:15
Uptime: 4.75 hours
```

## 🚀 Startup Management

### Example 14: Listing Startup Applications

```
You: Show startup apps

KernelSense:
Found 5 startup application(s):

  • Spotify.lnk
    C:\Users\User\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Spotify.lnk
  • Discord.lnk
    C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\Discord.lnk
```

## 🆘 Getting Help

### Example 15: Help Command

```
You: help

KernelSense:
🧠 KernelSense - Available Commands

System Diagnostics:
  • "Why is my computer slow?" - Diagnose performance issues
  • "Show CPU usage" - Display CPU information
  • "Check RAM" / "Check memory" - Display memory usage
  • "Show disk space" - Display disk usage
  • "Check network" - Display network statistics
  • "System overview" - Display overall system information

Process Management:
  • "List processes" - Show running processes
  • "Show top processes by CPU" - List CPU-intensive processes
  • "Find process using memory" - Find memory-intensive processes
  • "Kill process 1234" - Stop a process by PID
  • "Stop process named chrome" - Stop a process by name
  • "Show info for process 1234" - Get detailed process information

[... more commands ...]
```

## 🔄 Session Management

### Example 16: Exiting KernelSense

```
You: exit

KernelSense:
Goodbye! 👋

Session Summary:
  • Total operations: 12
  • Successful: 10
  • Failed: 2
  • Operations requiring approval: 2
    - Approved: 1
    - Denied: 1
```

## 📝 Audit Log Example

After running several commands, check `logs/kernelsense_20260928.log`:

```
================================================================================
[2026-09-28 10:30:15] SESSION START
================================================================================
[2026-09-28 10:30:23] USER INPUT: why is my computer slow?
[2026-09-28 10:30:24] Intent: diagnose_slowness | Success: True | Risk: SAFE | Result: System Status: WARNING...
[2026-09-28 10:31:15] USER INPUT: list processes
[2026-09-28 10:31:16] Intent: list_processes | Success: True | Risk: SAFE | Params: sort_by=memory, limit=10 | Result: Top 10 processes...
[2026-09-28 10:32:45] USER INPUT: kill process 8765
[2026-09-28 10:32:45] Intent: kill_process | Success: True | Risk: HIGH | Approved: True | Params: pid=8765 | Result: Process 'python.exe' stopped
[2026-09-28 10:33:30] SESSION END
================================================================================
```

## 🎯 Tips for Best Results

### Natural Language Variations

KernelSense understands many ways to ask the same thing:

**For CPU information:**
- "Show CPU"
- "Check CPU usage"
- "What's my processor doing?"
- "CPU status"

**For memory:**
- "Check RAM"
- "How much memory?"
- "Show memory usage"
- "RAM status"

**For processes:**
- "List processes"
- "What's running?"
- "Show running apps"
- "Active processes"

### Getting Specific Information

Be as specific as needed:
- "Top 5 processes" → limits results to 5
- "Process 1234" → targets specific PID
- "Find .txt files" → searches by extension
- "Python files" → searches by common type

### Safety First

Always:
1. Read warning messages completely
2. Understand consequences before approving
3. Review audit logs periodically
4. Test risky operations in safe environments first

---

**Need more help?** Type `help` in KernelSense for a quick command reference!
