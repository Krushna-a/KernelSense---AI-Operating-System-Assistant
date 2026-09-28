"""
Risk Assessor
Evaluates the risk level of operations and determines if user approval is needed
"""

from enum import Enum
from typing import Dict, Any, List
from core.intent_parser import Intent

class RiskLevel(Enum):
    """Risk levels for operations"""
    SAFE = "SAFE"           # No risk, can execute automatically
    LOW = "LOW"             # Minimal risk, can execute with logging
    MEDIUM = "MEDIUM"       # Some risk, requires user awareness
    HIGH = "HIGH"           # Significant risk, requires explicit approval
    CRITICAL = "CRITICAL"   # Destructive operation, requires confirmation

class RiskAssessor:
    """Assesses the risk level of operations"""
    
    # Define risk levels for different intents
    INTENT_RISK_LEVELS = {
        # Safe operations (read-only)
        Intent.CHECK_CPU: RiskLevel.SAFE,
        Intent.CHECK_MEMORY: RiskLevel.SAFE,
        Intent.CHECK_DISK: RiskLevel.SAFE,
        Intent.CHECK_NETWORK: RiskLevel.SAFE,
        Intent.SYSTEM_OVERVIEW: RiskLevel.SAFE,
        Intent.LIST_PROCESSES: RiskLevel.SAFE,
        Intent.FIND_PROCESS: RiskLevel.SAFE,
        Intent.PROCESS_INFO: RiskLevel.SAFE,
        Intent.DIAGNOSE_SLOWNESS: RiskLevel.SAFE,
        Intent.HELP: RiskLevel.SAFE,
        Intent.EXIT: RiskLevel.SAFE,
        Intent.UNKNOWN: RiskLevel.SAFE,
        
        # Low risk operations (some system interaction)
        Intent.LIST_STARTUP_APPS: RiskLevel.LOW,
        Intent.CHECK_SERVICES: RiskLevel.LOW,
        Intent.FIND_FILES: RiskLevel.LOW,
        Intent.SEARCH_CONTENT: RiskLevel.LOW,
        
        # High risk operations (can modify system)
        Intent.KILL_PROCESS: RiskLevel.HIGH,
        
        # Critical operations (destructive)
        Intent.DELETE_FILE: RiskLevel.CRITICAL,
    }
    
    # System-critical process names that should never be killed without warning
    CRITICAL_PROCESSES = {
        'system', 'registry', 'smss.exe', 'csrss.exe', 'wininit.exe', 
        'services.exe', 'lsass.exe', 'svchost.exe', 'explorer.exe',
        'dwm.exe', 'winlogon.exe', 'systemd', 'init', 'kernel',
        'launchd', 'loginwindow'
    }
    
    @staticmethod
    def assess_risk(intent: Intent, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess the risk level of an operation
        
        Args:
            intent: The user's intent
            parameters: Parameters for the operation
            
        Returns:
            Dictionary with 'risk_level', 'requires_approval', 'warning', 'consequences'
        """
        base_risk = RiskAssessor.INTENT_RISK_LEVELS.get(intent, RiskLevel.MEDIUM)
        
        # Adjust risk based on parameters
        adjusted_risk, warning, consequences = RiskAssessor._adjust_risk_for_parameters(
            intent, base_risk, parameters
        )
        
        requires_approval = adjusted_risk in [RiskLevel.HIGH, RiskLevel.CRITICAL]
        
        return {
            'risk_level': adjusted_risk,
            'requires_approval': requires_approval,
            'warning': warning,
            'consequences': consequences
        }
    
    @staticmethod
    def _adjust_risk_for_parameters(
        intent: Intent, 
        base_risk: RiskLevel, 
        parameters: Dict[str, Any]
    ) -> tuple:
        """
        Adjust risk level based on operation parameters
        
        Returns:
            Tuple of (adjusted_risk_level, warning_message, consequences_list)
        """
        warning = None
        consequences = []
        
        if intent == Intent.KILL_PROCESS:
            # Check if it's a critical system process
            process_name = parameters.get('name', '').lower()
            
            if process_name in RiskAssessor.CRITICAL_PROCESSES:
                base_risk = RiskLevel.CRITICAL
                warning = f"⚠️ '{process_name}' is a critical system process!"
                consequences = [
                    "System may become unstable",
                    "You may lose unsaved work",
                    "System restart may be required",
                    "Windows/System may crash"
                ]
            else:
                warning = "Stopping this process may cause data loss or application crashes."
                consequences = [
                    "Application will close immediately",
                    "Unsaved work will be lost",
                    "Related processes may be affected"
                ]
        
        elif intent == Intent.DELETE_FILE:
            path = parameters.get('path', '')
            
            # Check for system directories
            system_paths = ['windows', 'system32', 'program files', '/etc', '/bin', '/usr', '/sys']
            if any(sys_path in path.lower() for sys_path in system_paths):
                warning = "⚠️ This file is in a system directory!"
                consequences = [
                    "System files may be corrupted",
                    "Applications may stop working",
                    "System may become unstable",
                    "Recovery may be difficult"
                ]
            else:
                warning = "This file will be permanently deleted."
                consequences = [
                    "File cannot be recovered",
                    "Deletion is immediate and permanent"
                ]
        
        return base_risk, warning, consequences
    
    @staticmethod
    def validate_operation(intent: Intent, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate if an operation can be executed
        
        Args:
            intent: The user's intent
            parameters: Parameters for the operation
            
        Returns:
            Dictionary with 'valid', 'message'
        """
        # Validate based on intent
        if intent == Intent.KILL_PROCESS:
            if 'pid' not in parameters and 'name' not in parameters:
                return {
                    'valid': False,
                    'message': "Process ID (PID) or process name is required to kill a process."
                }
        
        elif intent == Intent.DELETE_FILE:
            if 'path' not in parameters:
                return {
                    'valid': False,
                    'message': "File path is required to delete a file."
                }
        
        elif intent == Intent.PROCESS_INFO:
            if 'pid' not in parameters:
                return {
                    'valid': False,
                    'message': "Process ID (PID) is required to get process information."
                }
        
        # All validations passed
        return {
            'valid': True,
            'message': None
        }
    
    @staticmethod
    def get_risk_description(risk_level: RiskLevel) -> str:
        """Get a human-readable description of a risk level"""
        descriptions = {
            RiskLevel.SAFE: "✓ Safe operation - read-only access",
            RiskLevel.LOW: "ℹ️ Low risk - minimal system interaction",
            RiskLevel.MEDIUM: "⚠️ Medium risk - system changes possible",
            RiskLevel.HIGH: "⚠️ HIGH RISK - significant system changes",
            RiskLevel.CRITICAL: "🔴 CRITICAL RISK - destructive operation"
        }
        return descriptions.get(risk_level, "Unknown risk level")
