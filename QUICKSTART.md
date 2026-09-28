# KernelSense Quick Start Guide

Get started with KernelSense in 3 easy steps!

## 🚀 Quick Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `psutil` - System information library
- `colorama` - Colored terminal output

### Step 2: Run KernelSense

```bash
python kernelsense.py
```

### Step 3: Try Your First Commands

```
You: help
```

See all available commands and examples.

## 💡 Try These Commands

### Check System Health
```
You: Why is my computer slow?
```

### View Resources
```
You: Show CPU usage
You: Check RAM
You: Show disk space
```

### Manage Processes
```
You: List processes
You: Show top processes by CPU
```

### Get System Info
```
You: System overview
```

## 🎯 Common Use Cases

### 1. Finding Memory Hogs
```
You: List processes
```
Look at the "Memory MB" column to see which process is using the most RAM.

### 2. Quick Performance Check
```
You: Why is my computer slow?
```
KernelSense automatically checks CPU, RAM, disk, and identifies issues.

### 3. Finding Files
```
You: Find Python files
You: Find files named config.txt
```

### 4. Stopping Unresponsive Programs
```
You: List processes
# Note the PID of the unresponsive process
You: Kill process [PID]
# Confirm when prompted
```

## ⚠️ Important Safety Tips

1. **Read warnings carefully** before approving operations
2. **Start with safe commands** like "check CPU" or "list processes"
3. **Test risky operations carefully** - especially killing processes
4. **Check audit logs** in the `logs/` folder to review your actions

## 📚 Need More Help?

- **In-app help**: Type `help` in KernelSense
- **Detailed examples**: See `EXAMPLES.md`
- **Full documentation**: See `README.md`
- **Architecture**: See `ARCHITECTURE.md` for technical details

## 🎓 Learning Path

### Beginner (Safe Commands)
1. `help` - See what's available
2. `show CPU usage` - View CPU info
3. `check RAM` - View memory usage
4. `list processes` - See running programs
5. `system overview` - Get full system info

### Intermediate (Read-Only Operations)
1. `why is my computer slow?` - Diagnose issues
2. `show top processes by CPU` - Find CPU hogs
3. `find Python files` - Search for files
4. `check disk space` - View disk usage
5. `show startup apps` - See what runs at startup

### Advanced (Operations Requiring Approval)
1. `kill process [PID]` - Stop a process
2. `stop process named [name]` - Stop by name

**Remember:** Always approve carefully and read consequences!

## 🛠️ Troubleshooting Quick Fixes

### "Access Denied" when killing a process
→ Run as Administrator (Windows) or use sudo (Linux/Mac)

### Colors not showing
→ Make sure colorama is installed: `pip install colorama`

### "Module not found" error
→ Install dependencies: `pip install -r requirements.txt`

### Process not found
→ Use `list processes` to see available PIDs

## 🎉 You're Ready!

Start KernelSense and try asking about your system in natural language. No commands to memorize - just ask!

```bash
python kernelsense.py
```

Happy system monitoring! 🧠
