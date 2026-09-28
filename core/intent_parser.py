"""
Intent Parser
Interprets natural language requests and determines user intent
"""

import re
from typing import Dict, Any, Optional
from enum import Enum

class Intent(Enum):
    """Enumeration of possible user intents"""
    # System diagnostics
    DIAGNOSE_SLOWNESS = "diagnose_slowness"
    CHECK_CPU = "check_cpu"
    CHECK_MEMORY = "check_memory"
    CHECK_DISK = "check_disk"
    CHECK_NETWORK = "check_network"
    SYSTEM_OVERVIEW = "system_overview"
    
    # Process management
    LIST_PROCESSES = "list_processes"
    FIND_PROCESS = "find_process"
    KILL_PROCESS = "kill_process"
    PROCESS_INFO = "process_info"
    
    # File operations
    FIND_FILES = "find_files"
    DELETE_FILE = "delete_file"
    SEARCH_CONTENT = "search_content"
    
    # System operations
    LIST_STARTUP_APPS = "list_startup_apps"
    CHECK_SERVICES = "check_services"
    
    # General
    HELP = "help"
    EXIT = "exit"
    UNKNOWN = "unknown"

class IntentParser:
    """Parses natural language input to determine user intent"""
    
    # Pattern definitions for intent matching
    PATTERNS = {
        Intent.DIAGNOSE_SLOWNESS: [
            r'\b(why|what|how|diagnose|check|find|investigate).*(slow|slowness|sluggish|lagging|lag|performance|hang|freeze|unresponsive)',
            r'\b(slow|sluggish|lagging|performance).*(issue|problem|cause|reason)',
            r'\b(system|computer|pc|machine).*(slow|performance)',
        ],
        Intent.CHECK_CPU: [
            r'\b(show|check|what|display|get|view).*(cpu|processor|core)',
            r'\b(cpu|processor).*(usage|use|utilization|load)',
            r'\bhow much.*(cpu|processor)',
        ],
        Intent.CHECK_MEMORY: [
            r'\b(show|check|what|display|get|view).*(ram|memory)',
            r'\b(ram|memory).*(usage|use|available|free)',
            r'\bhow much.*(ram|memory)',
        ],
        Intent.CHECK_DISK: [
            r'\b(show|check|what|display|get|view).*(disk|storage|drive|space)',
            r'\b(disk|storage).*(usage|use|space|full|free)',
            r'\bhow much.*(disk|storage|space)',
        ],
        Intent.CHECK_NETWORK: [
            r'\b(show|check|what|display|get|view).*(network|internet|connection)',
            r'\b(network|internet).*(usage|traffic|speed|bandwidth)',
        ],
        Intent.SYSTEM_OVERVIEW: [
            r'\b(show|display|get|view).*(system|overview|summary|status|info)',
            r'\bsystem\s+(info|information|details)',
            r'\b(what|show).*(running|system)',
        ],
        Intent.LIST_PROCESSES: [
            r'\b(list|show|display|get|view).*(process|processes|running|task)',
            r'\bwhat.*(running|processes)',
            r'\b(running|active).*(process|processes|application)',
        ],
        Intent.FIND_PROCESS: [
            r'\bfind.*(process|application|program|app)',
            r'\b(which|what).*(process|application|program).*\b(using|consuming|taking)',
        ],
        Intent.KILL_PROCESS: [
            r'\b(kill|stop|terminate|end|close).*(process|application|program|task)',
        ],
        Intent.PROCESS_INFO: [
            r'\b(info|information|details|show).*(process|pid)',
            r'\bprocess\s+\d+',
        ],
        Intent.FIND_FILES: [
            r'\b(find|search|locate|look).*(file|files)',
            r'\bwhere.*(file|files)',
        ],
        Intent.DELETE_FILE: [
            r'\b(delete|remove|erase).*(file|folder|directory)',
        ],
        Intent.SEARCH_CONTENT: [
            r'\b(search|find|look).*(content|text|string|word)',
            r'\bgrep',
        ],
        Intent.LIST_STARTUP_APPS: [
            r'\b(startup|autostart|boot).*(app|application|program)',
            r'\bwhat.*(start|startup).*automatically',
        ],
        Intent.CHECK_SERVICES: [
            r'\b(show|list|check).*(service|services|daemon)',
        ],
        Intent.HELP: [
            r'\b(help|what can you|commands|capabilities)',
        ],
        Intent.EXIT: [
            r'\b(exit|quit|bye|goodbye|close)',
        ],
    }
    
    @staticmethod
    def parse(user_input: str) -> Dict[str, Any]:
        """
        Parse user input and return intent with parameters
        
        Returns:
            Dict containing 'intent', 'confidence', and 'parameters'
        """
        user_input = user_input.lower().strip()
        
        # Check for exact matches first
        if not user_input or user_input in ['exit', 'quit', 'bye']:
            return {
                'intent': Intent.EXIT,
                'confidence': 1.0,
                'parameters': {}
            }
        
        if user_input in ['help', '?']:
            return {
                'intent': Intent.HELP,
                'confidence': 1.0,
                'parameters': {}
            }
        
        # Try to match patterns
        best_match = None
        best_confidence = 0.0
        
        for intent, patterns in IntentParser.PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    # Calculate confidence based on match quality
                    confidence = len(match.group(0)) / len(user_input)
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = intent
        
        if best_match:
            parameters = IntentParser._extract_parameters(user_input, best_match)
            return {
                'intent': best_match,
                'confidence': best_confidence,
                'parameters': parameters
            }
        
        # No match found
        return {
            'intent': Intent.UNKNOWN,
            'confidence': 0.0,
            'parameters': {'original_input': user_input}
        }
    
    @staticmethod
    def _extract_parameters(user_input: str, intent: Intent) -> Dict[str, Any]:
        """Extract parameters from user input based on intent"""
        parameters = {}
        
        if intent == Intent.KILL_PROCESS:
            # Try to extract PID
            pid_match = re.search(r'\b(pid\s*)?(\d+)\b', user_input, re.IGNORECASE)
            if pid_match:
                parameters['pid'] = int(pid_match.group(2))
            
            # Try to extract process name
            name_match = re.search(r'["\']([^"\']+)["\']|(?:named?|called)\s+(\w+)', user_input, re.IGNORECASE)
            if name_match:
                parameters['name'] = name_match.group(1) or name_match.group(2)
        
        elif intent == Intent.FIND_FILES:
            # Extract file pattern or name
            pattern_match = re.search(r'["\']([^"\']+)["\']|\b(\w+\.\w+)\b', user_input)
            if pattern_match:
                parameters['pattern'] = pattern_match.group(1) or pattern_match.group(2)
            
            # Extract file type
            type_match = re.search(r'\b(python|java|javascript|text|\.[\w]+)\s+files?\b', user_input, re.IGNORECASE)
            if type_match:
                file_type = type_match.group(1).lower()
                if not file_type.startswith('.'):
                    # Map common types to extensions
                    type_map = {
                        'python': '.py',
                        'java': '.java',
                        'javascript': '.js',
                        'text': '.txt'
                    }
                    file_type = type_map.get(file_type, file_type)
                parameters['file_type'] = file_type
        
        elif intent == Intent.LIST_PROCESSES:
            # Check if sorting preference is specified
            if re.search(r'\b(memory|ram)\b', user_input, re.IGNORECASE):
                parameters['sort_by'] = 'memory'
            elif re.search(r'\b(cpu|processor)\b', user_input, re.IGNORECASE):
                parameters['sort_by'] = 'cpu'
            else:
                parameters['sort_by'] = 'memory'  # Default
            
            # Check if limit is specified
            limit_match = re.search(r'\b(top|first)\s+(\d+)\b', user_input, re.IGNORECASE)
            if limit_match:
                parameters['limit'] = int(limit_match.group(2))
            else:
                parameters['limit'] = 10  # Default
        
        elif intent == Intent.PROCESS_INFO:
            # Extract PID
            pid_match = re.search(r'\b(\d+)\b', user_input)
            if pid_match:
                parameters['pid'] = int(pid_match.group(1))
        
        elif intent == Intent.DELETE_FILE:
            # Extract file path
            path_match = re.search(r'["\']([^"\']+)["\']', user_input)
            if path_match:
                parameters['path'] = path_match.group(1)
        
        return parameters
    
    @staticmethod
    def get_help_text() -> str:
        """Return help text showing available commands"""
        return """
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

File Operations:
  • "Find Python files" - Search for files by type
  • "Find files named test.txt" - Search for specific files

Other:
  • "help" - Show this help message
  • "exit" / "quit" - Exit KernelSense

Just type your question in natural language!
        """
