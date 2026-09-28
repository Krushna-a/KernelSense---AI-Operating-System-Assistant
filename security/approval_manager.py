"""
Approval Manager
Manages user approval for dangerous operations
"""

from typing import Dict, Any, Optional
from datetime import datetime
from core.intent_parser import Intent
from security.risk_assessor import RiskLevel

class ApprovalManager:
    """Manages user approvals for risky operations"""
    
    def __init__(self):
        """Initialize the approval manager"""
        self.approval_history = []
    
    def request_approval(
        self, 
        intent: Intent, 
        parameters: Dict[str, Any],
        risk_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Request user approval for an operation
        
        Args:
            intent: The user's intent
            parameters: Parameters for the operation
            risk_info: Risk assessment information
            
        Returns:
            Dictionary with 'approved', 'timestamp', 'user_response'
        """
        # This is a placeholder - actual approval is handled by the CLI
        # This method records the approval request
        
        request = {
            'intent': intent,
            'parameters': parameters,
            'risk_level': risk_info['risk_level'],
            'timestamp': datetime.now(),
            'warning': risk_info['warning'],
            'consequences': risk_info['consequences']
        }
        
        return request
    
    def record_decision(
        self,
        intent: Intent,
        parameters: Dict[str, Any],
        approved: bool,
        risk_level: RiskLevel,
        user_response: str = None
    ) -> None:
        """
        Record a user's approval decision
        
        Args:
            intent: The operation intent
            parameters: Operation parameters
            approved: Whether the user approved
            risk_level: The risk level of the operation
            user_response: The user's response text
        """
        record = {
            'timestamp': datetime.now(),
            'intent': intent.value,
            'parameters': parameters,
            'approved': approved,
            'risk_level': risk_level.value,
            'user_response': user_response
        }
        
        self.approval_history.append(record)
    
    def get_approval_stats(self) -> Dict[str, Any]:
        """
        Get statistics about approval history
        
        Returns:
            Dictionary with approval statistics
        """
        if not self.approval_history:
            return {
                'total_requests': 0,
                'approved': 0,
                'denied': 0,
                'approval_rate': 0.0
            }
        
        total = len(self.approval_history)
        approved = sum(1 for r in self.approval_history if r['approved'])
        denied = total - approved
        
        return {
            'total_requests': total,
            'approved': approved,
            'denied': denied,
            'approval_rate': round((approved / total) * 100, 2) if total > 0 else 0.0
        }
    
    def get_recent_decisions(self, limit: int = 10) -> list:
        """
        Get recent approval decisions
        
        Args:
            limit: Maximum number of decisions to return
            
        Returns:
            List of recent decision records
        """
        return self.approval_history[-limit:]

class ApprovalPrompt:
    """Handles interactive approval prompts"""
    
    @staticmethod
    def get_user_approval(prompt_text: str) -> tuple:
        """
        Display approval prompt and get user response
        
        Args:
            prompt_text: The approval prompt to display
            
        Returns:
            Tuple of (approved: bool, user_response: str)
        """
        print(prompt_text)
        print()
        
        while True:
            response = input("Do you want to proceed? (yes/no): ").strip().lower()
            
            if response in ['yes', 'y']:
                return True, response
            elif response in ['no', 'n']:
                return False, response
            else:
                print("Please enter 'yes' or 'no'.")
    
    @staticmethod
    def get_confirmation_with_details(
        operation: str,
        details: list,
        risk_level: RiskLevel
    ) -> tuple:
        """
        Get detailed confirmation from user
        
        Args:
            operation: Description of the operation
            details: List of detail strings to display
            risk_level: The risk level of the operation
            
        Returns:
            Tuple of (approved: bool, user_response: str)
        """
        print()
        print("=" * 60)
        print(f"CONFIRMATION REQUIRED - {risk_level.value}")
        print("=" * 60)
        print()
        print(f"Operation: {operation}")
        print()
        
        if details:
            print("Details:")
            for detail in details:
                print(f"  • {detail}")
            print()
        
        print("=" * 60)
        
        return ApprovalPrompt.get_user_approval("")
