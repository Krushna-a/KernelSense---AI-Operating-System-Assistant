"""
Security Validator
Validates operations before execution and manages security checks
"""

from typing import Dict, Any
from core.intent_parser import Intent
from security.risk_assessor import RiskAssessor, RiskLevel

class SecurityValidator:
    """Validates operations for security and safety"""
    
    def __init__(self):
        """Initialize the security validator"""
        self.risk_assessor = RiskAssessor()
    
    def validate_and_assess(self, intent: Intent, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate an operation and assess its risk
        
        Args:
            intent: The user's intent
            parameters: Parameters for the operation
            
        Returns:
            Dictionary with validation and risk assessment results
        """
        # First, validate the operation
        validation = self.risk_assessor.validate_operation(intent, parameters)
        
        if not validation['valid']:
            return {
                'valid': False,
                'approved': False,
                'message': validation['message'],
                'risk_level': None,
                'requires_approval': False,
                'warning': None,
                'consequences': []
            }
        
        # Then assess risk
        risk_assessment = self.risk_assessor.assess_risk(intent, parameters)
        
        return {
            'valid': True,
            'approved': not risk_assessment['requires_approval'],  # Auto-approve if no approval needed
            'message': None,
            'risk_level': risk_assessment['risk_level'],
            'requires_approval': risk_assessment['requires_approval'],
            'warning': risk_assessment['warning'],
            'consequences': risk_assessment['consequences']
        }
    
    def get_approval_prompt(self, intent: Intent, parameters: Dict[str, Any], risk_info: Dict[str, Any]) -> str:
        """
        Generate an approval prompt for risky operations
        
        Args:
            intent: The user's intent
            parameters: Parameters for the operation
            risk_info: Risk assessment information
            
        Returns:
            Formatted approval prompt string
        """
        risk_level = risk_info['risk_level']
        warning = risk_info['warning']
        consequences = risk_info['consequences']
        
        prompt = [
            "",
            "=" * 60,
            self.risk_assessor.get_risk_description(risk_level),
            "=" * 60,
            ""
        ]
        
        # Add operation description
        if intent == Intent.KILL_PROCESS:
            pid = parameters.get('pid')
            name = parameters.get('name')
            if pid:
                prompt.append(f"Operation: Stop process with PID {pid}")
            elif name:
                prompt.append(f"Operation: Stop process named '{name}'")
        elif intent == Intent.DELETE_FILE:
            path = parameters.get('path')
            prompt.append(f"Operation: Delete file '{path}'")
        
        # Add warning
        if warning:
            prompt.append("")
            prompt.append(warning)
        
        # Add consequences
        if consequences:
            prompt.append("")
            prompt.append("Potential consequences:")
            for consequence in consequences:
                prompt.append(f"  • {consequence}")
        
        prompt.append("")
        prompt.append("=" * 60)
        
        return "\n".join(prompt)
    
    def check_permission(self, intent: Intent) -> bool:
        """
        Check if the application has permission to perform an operation
        
        Args:
            intent: The user's intent
            
        Returns:
            True if permission is available, False otherwise
        """
        # This is a simplified check. In a real system, you'd check actual permissions.
        # For now, we'll assume we have permission for most operations.
        
        # Operations that typically require elevated privileges
        elevated_operations = [Intent.CHECK_SERVICES]
        
        if intent in elevated_operations:
            # In a real implementation, check if running as admin/root
            # For now, we'll return True
            return True
        
        return True
