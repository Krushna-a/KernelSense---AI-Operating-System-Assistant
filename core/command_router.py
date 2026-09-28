"""
Command Router
Routes parsed intents to appropriate handlers
"""

from typing import Dict, Any, Callable
from core.intent_parser import Intent, IntentParser
from core.operations import SystemOperations
from system_info.collector import SystemInfoCollector
from system_info.formatters import SystemInfoFormatter

class CommandRouter:
    """Routes commands to appropriate handlers"""
    
    def __init__(self):
        """Initialize the command router"""
        self.handlers = {
            Intent.DIAGNOSE_SLOWNESS: self._handle_diagnose_slowness,
            Intent.CHECK_CPU: self._handle_check_cpu,
            Intent.CHECK_MEMORY: self._handle_check_memory,
            Intent.CHECK_DISK: self._handle_check_disk,
            Intent.CHECK_NETWORK: self._handle_check_network,
            Intent.SYSTEM_OVERVIEW: self._handle_system_overview,
            Intent.LIST_PROCESSES: self._handle_list_processes,
            Intent.FIND_PROCESS: self._handle_find_process,
            Intent.PROCESS_INFO: self._handle_process_info,
            Intent.KILL_PROCESS: self._handle_kill_process,
            Intent.FIND_FILES: self._handle_find_files,
            Intent.DELETE_FILE: self._handle_delete_file,
            Intent.LIST_STARTUP_APPS: self._handle_list_startup_apps,
            Intent.SEARCH_CONTENT: self._handle_search_content,
            Intent.HELP: self._handle_help,
            Intent.UNKNOWN: self._handle_unknown,
        }
        
        self.collector = SystemInfoCollector()
        self.formatter = SystemInfoFormatter()
        self.operations = SystemOperations()
    
    def route(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route a parsed intent to the appropriate handler
        
        Args:
            intent_data: Dictionary containing 'intent', 'confidence', and 'parameters'
            
        Returns:
            Dictionary containing 'success', 'message', 'data', and 'requires_approval'
        """
        intent = intent_data['intent']
        parameters = intent_data['parameters']
        
        handler = self.handlers.get(intent, self._handle_unknown)
        
        try:
            return handler(parameters)
        except Exception as e:
            return {
                'success': False,
                'message': f"Error executing command: {str(e)}",
                'data': None,
                'requires_approval': False
            }
    
    # Handler methods
    
    def _handle_diagnose_slowness(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle system slowness diagnosis"""
        diagnosis = self.collector.diagnose_slowness()
        formatted = self.formatter.format_diagnosis(diagnosis)
        
        return {
            'success': True,
            'message': formatted,
            'data': diagnosis,
            'requires_approval': False
        }
    
    def _handle_check_cpu(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle CPU check request"""
        cpu_info = self.collector.get_cpu_info()
        formatted = self.formatter.format_cpu_info(cpu_info)
        
        return {
            'success': True,
            'message': formatted,
            'data': cpu_info,
            'requires_approval': False
        }
    
    def _handle_check_memory(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle memory check request"""
        mem_info = self.collector.get_memory_info()
        formatted = self.formatter.format_memory_info(mem_info)
        
        return {
            'success': True,
            'message': formatted,
            'data': mem_info,
            'requires_approval': False
        }
    
    def _handle_check_disk(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle disk check request"""
        disk_info = self.collector.get_disk_info()
        formatted = self.formatter.format_disk_info(disk_info)
        
        return {
            'success': True,
            'message': formatted,
            'data': disk_info,
            'requires_approval': False
        }
    
    def _handle_check_network(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle network check request"""
        net_info = self.collector.get_network_info()
        formatted = self.formatter.format_network_info(net_info)
        
        return {
            'success': True,
            'message': formatted,
            'data': net_info,
            'requires_approval': False
        }
    
    def _handle_system_overview(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle system overview request"""
        overview = self.collector.get_system_overview()
        formatted = self.formatter.format_system_overview(overview)
        
        return {
            'success': True,
            'message': formatted,
            'data': overview,
            'requires_approval': False
        }
    
    def _handle_list_processes(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list processes request"""
        sort_by = params.get('sort_by', 'memory')
        limit = params.get('limit', 10)
        
        processes = self.collector.get_process_list(sort_by=sort_by, limit=limit)
        formatted = self.formatter.format_process_list(processes)
        
        message = f"Top {limit} processes by {sort_by}:\n\n{formatted}"
        
        return {
            'success': True,
            'message': message,
            'data': processes,
            'requires_approval': False
        }
    
    def _handle_find_process(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle find process request"""
        # Default to finding memory-intensive processes
        processes = self.collector.get_process_list(sort_by='memory', limit=5)
        formatted = self.formatter.format_process_list(processes)
        
        message = f"Top memory-consuming processes:\n\n{formatted}"
        
        return {
            'success': True,
            'message': message,
            'data': processes,
            'requires_approval': False
        }
    
    def _handle_process_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle process info request"""
        pid = params.get('pid')
        
        if not pid:
            return {
                'success': False,
                'message': "Please specify a process ID (PID).",
                'data': None,
                'requires_approval': False
            }
        
        proc_info = self.collector.get_specific_process(pid)
        
        if 'error' in proc_info:
            return {
                'success': False,
                'message': f"Could not get process information: {proc_info['error']}",
                'data': None,
                'requires_approval': False
            }
        
        # Format process info
        message = f"""
Process Information:
  PID: {proc_info['pid']}
  Name: {proc_info['name']}
  Status: {proc_info['status']}
  Username: {proc_info['username']}
  Created: {proc_info['create_time']}
  CPU Usage: {proc_info['cpu_percent']}%
  Memory: {proc_info['memory_mb']} MB ({proc_info['memory_percent']}%)
  Threads: {proc_info['num_threads']}
  Working Directory: {proc_info['cwd']}
  Executable: {proc_info['exe']}
  Command Line: {proc_info['cmdline'] or 'N/A'}
        """
        
        return {
            'success': True,
            'message': message.strip(),
            'data': proc_info,
            'requires_approval': False
        }
    
    def _handle_help(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle help request"""
        help_text = IntentParser.get_help_text()
        
        return {
            'success': True,
            'message': help_text,
            'data': None,
            'requires_approval': False
        }
    
    def _handle_kill_process(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle kill process request"""
        pid = params.get('pid')
        name = params.get('name')
        
        if pid:
            result = self.operations.kill_process_by_pid(pid)
        elif name:
            result = self.operations.kill_process_by_name(name)
        else:
            return {
                'success': False,
                'message': "Please specify a process ID (PID) or process name to stop.",
                'data': None,
                'requires_approval': True
            }
        
        return {
            'success': result['success'],
            'message': result['message'],
            'data': result,
            'requires_approval': True
        }
    
    def _handle_find_files(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle find files request"""
        pattern = params.get('pattern', '')
        file_type = params.get('file_type')
        
        result = self.operations.find_files(
            pattern=pattern,
            file_type=file_type
        )
        
        return {
            'success': result['success'],
            'message': result['message'],
            'data': result.get('files'),
            'requires_approval': False
        }
    
    def _handle_delete_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle delete file request"""
        path = params.get('path')
        
        if not path:
            return {
                'success': False,
                'message': "Please specify a file path to delete.",
                'data': None,
                'requires_approval': True
            }
        
        result = self.operations.delete_file(path)
        
        return {
            'success': result['success'],
            'message': result['message'],
            'data': None,
            'requires_approval': True
        }
    
    def _handle_list_startup_apps(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list startup apps request"""
        result = self.operations.get_startup_apps()
        
        return {
            'success': result['success'],
            'message': result['message'],
            'data': result.get('apps'),
            'requires_approval': False
        }
    
    def _handle_search_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle search content request"""
        pattern = params.get('pattern', '')
        file_type = params.get('file_type')
        
        if not pattern:
            return {
                'success': False,
                'message': "Please specify a search pattern.",
                'data': None,
                'requires_approval': False
            }
        
        result = self.operations.search_file_content(
            pattern=pattern,
            file_type=file_type
        )
        
        return {
            'success': result['success'],
            'message': result['message'],
            'data': result.get('results'),
            'requires_approval': False
        }
    
    def _handle_unknown(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle unknown intent"""
        original_input = params.get('original_input', '')
        
        message = f"""
I'm not sure how to help with: "{original_input}"

Try asking things like:
  • "Why is my computer slow?"
  • "Show CPU usage"
  • "List processes"
  • "Check disk space"

Type "help" for more commands.
        """
        
        return {
            'success': False,
            'message': message.strip(),
            'data': None,
            'requires_approval': False
        }
