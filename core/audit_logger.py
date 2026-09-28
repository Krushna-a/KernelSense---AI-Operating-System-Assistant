"""
Audit Logger
Comprehensive logging system for all KernelSense operations
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class AuditLogger:
    """Logs all operations for audit trail"""
    
    def __init__(self, log_dir: str = "logs"):
        """
        Initialize the audit logger
        
        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create log file with current date
        self.log_file = self.log_dir / f"kernelsense_{datetime.now().strftime('%Y%m%d')}.log"
        self.json_log_file = self.log_dir / f"kernelsense_{datetime.now().strftime('%Y%m%d')}.json"
        
        # Initialize JSON log if it doesn't exist
        if not self.json_log_file.exists():
            with open(self.json_log_file, 'w') as f:
                json.dump([], f)
    
    def log_operation(
        self,
        intent: str,
        parameters: Dict[str, Any],
        success: bool,
        risk_level: Optional[str] = None,
        approved: Optional[bool] = None,
        result: Optional[str] = None,
        error: Optional[str] = None
    ) -> None:
        """
        Log an operation to the audit trail
        
        Args:
            intent: The operation intent
            parameters: Operation parameters
            success: Whether the operation succeeded
            risk_level: Risk level of the operation
            approved: Whether user approval was given (if required)
            result: Result message
            error: Error message if operation failed
        """
        timestamp = datetime.now()
        
        # Create log entry
        log_entry = {
            'timestamp': timestamp.isoformat(),
            'intent': intent,
            'parameters': parameters,
            'success': success,
            'risk_level': risk_level,
            'approved': approved,
            'result': result,
            'error': error
        }
        
        # Write to text log
        self._write_text_log(log_entry, timestamp)
        
        # Write to JSON log
        self._write_json_log(log_entry)
    
    def _write_text_log(self, entry: Dict[str, Any], timestamp: datetime) -> None:
        """Write log entry to text file"""
        log_line = f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
        log_line += f"Intent: {entry['intent']} | "
        log_line += f"Success: {entry['success']} | "
        
        if entry['risk_level']:
            log_line += f"Risk: {entry['risk_level']} | "
        
        if entry['approved'] is not None:
            log_line += f"Approved: {entry['approved']} | "
        
        if entry['parameters']:
            params_str = ", ".join([f"{k}={v}" for k, v in entry['parameters'].items()])
            log_line += f"Params: {params_str} | "
        
        if entry['error']:
            log_line += f"Error: {entry['error']}"
        elif entry['result']:
            # Truncate long results
            result_preview = entry['result'][:100] + "..." if len(entry['result']) > 100 else entry['result']
            log_line += f"Result: {result_preview}"
        
        log_line += "\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
    
    def _write_json_log(self, entry: Dict[str, Any]) -> None:
        """Write log entry to JSON file"""
        try:
            # Read existing logs
            with open(self.json_log_file, 'r') as f:
                logs = json.load(f)
            
            # Append new entry
            logs.append(entry)
            
            # Write back
            with open(self.json_log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            # If JSON log fails, write to text log
            error_msg = f"Failed to write JSON log: {str(e)}\n"
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(error_msg)
    
    def log_user_input(self, user_input: str) -> None:
        """
        Log user input
        
        Args:
            user_input: The user's input text
        """
        timestamp = datetime.now()
        log_line = f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] USER INPUT: {user_input}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
    
    def log_error(self, error_message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an error
        
        Args:
            error_message: The error message
            context: Additional context about the error
        """
        timestamp = datetime.now()
        log_line = f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {error_message}"
        
        if context:
            log_line += f" | Context: {json.dumps(context)}"
        
        log_line += "\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
    
    def log_session_start(self) -> None:
        """Log the start of a new session"""
        timestamp = datetime.now()
        log_line = f"\n{'='*80}\n"
        log_line += f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] SESSION START\n"
        log_line += f"{'='*80}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
    
    def log_session_end(self) -> None:
        """Log the end of a session"""
        timestamp = datetime.now()
        log_line = f"\n[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] SESSION END\n"
        log_line += f"{'='*80}\n\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
    
    def get_recent_logs(self, limit: int = 20) -> list:
        """
        Get recent log entries
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of recent log entries
        """
        try:
            with open(self.json_log_file, 'r') as f:
                logs = json.load(f)
            return logs[-limit:]
        except Exception:
            return []
    
    def get_logs_by_date(self, date: datetime) -> list:
        """
        Get logs for a specific date
        
        Args:
            date: The date to get logs for
            
        Returns:
            List of log entries for that date
        """
        log_file = self.log_dir / f"kernelsense_{date.strftime('%Y%m%d')}.json"
        
        if not log_file.exists():
            return []
        
        try:
            with open(log_file, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics from audit logs
        
        Returns:
            Dictionary with log statistics
        """
        try:
            with open(self.json_log_file, 'r') as f:
                logs = json.load(f)
            
            if not logs:
                return {
                    'total_operations': 0,
                    'successful_operations': 0,
                    'failed_operations': 0,
                    'high_risk_operations': 0,
                    'operations_requiring_approval': 0,
                    'approved_operations': 0,
                    'denied_operations': 0
                }
            
            total = len(logs)
            successful = sum(1 for log in logs if log.get('success'))
            failed = total - successful
            high_risk = sum(1 for log in logs if log.get('risk_level') in ['HIGH', 'CRITICAL'])
            requiring_approval = sum(1 for log in logs if log.get('approved') is not None)
            approved = sum(1 for log in logs if log.get('approved') is True)
            denied = requiring_approval - approved
            
            return {
                'total_operations': total,
                'successful_operations': successful,
                'failed_operations': failed,
                'high_risk_operations': high_risk,
                'operations_requiring_approval': requiring_approval,
                'approved_operations': approved,
                'denied_operations': denied,
                'success_rate': round((successful / total * 100), 2) if total > 0 else 0
            }
        except Exception:
            return {
                'total_operations': 0,
                'successful_operations': 0,
                'failed_operations': 0,
                'high_risk_operations': 0,
                'operations_requiring_approval': 0,
                'approved_operations': 0,
                'denied_operations': 0,
                'success_rate': 0
            }
    
    def export_logs(self, output_file: str, start_date: Optional[datetime] = None, 
                    end_date: Optional[datetime] = None) -> bool:
        """
        Export logs to a file
        
        Args:
            output_file: Path to output file
            start_date: Start date for export (optional)
            end_date: End date for export (optional)
            
        Returns:
            True if export succeeded, False otherwise
        """
        try:
            logs = []
            
            # Collect logs from all dates in range
            if start_date and end_date:
                current_date = start_date
                while current_date <= end_date:
                    date_logs = self.get_logs_by_date(current_date)
                    logs.extend(date_logs)
                    current_date = current_date.replace(day=current_date.day + 1)
            else:
                with open(self.json_log_file, 'r') as f:
                    logs = json.load(f)
            
            # Export to file
            with open(output_file, 'w') as f:
                json.dump(logs, f, indent=2)
            
            return True
        except Exception as e:
            self.log_error(f"Failed to export logs: {str(e)}")
            return False
