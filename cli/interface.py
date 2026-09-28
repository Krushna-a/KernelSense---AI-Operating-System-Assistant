"""
KernelSense CLI Interface
User-friendly command-line interface with colored output
"""

import sys
from colorama import init, Fore, Style
from core.intent_parser import IntentParser, Intent
from core.command_router import CommandRouter
from core.audit_logger import AuditLogger
from security.validator import SecurityValidator
from security.approval_manager import ApprovalManager, ApprovalPrompt

# Initialize colorama for Windows
init(autoreset=True)

class KernelSenseCLI:
    """Interactive command-line interface for KernelSense"""
    
    def __init__(self):
        """Initialize the CLI"""
        self.parser = IntentParser()
        self.router = CommandRouter()
        self.validator = SecurityValidator()
        self.approval_manager = ApprovalManager()
        self.audit_logger = AuditLogger()
        self.running = True
    
    def run(self):
        """Main CLI loop"""
        self.audit_logger.log_session_start()
        
        self._print_welcome()
        
        while self.running:
            try:
                # Get user input
                user_input = self._get_user_input()
                
                if not user_input:
                    continue
                
                # Log user input
                self.audit_logger.log_user_input(user_input)
                
                # Parse intent
                intent_data = self.parser.parse(user_input)
                intent = intent_data['intent']
                parameters = intent_data['parameters']
                
                # Handle exit
                if intent == Intent.EXIT:
                    self._handle_exit()
                    break
                
                # Display intent confidence if low
                if intent_data['confidence'] < 0.5 and intent != Intent.UNKNOWN:
                    print(f"{Fore.YELLOW}ℹ️  Not sure I understood correctly. Interpreting as: {intent.value}{Style.RESET_ALL}")
                    print()
                
                # Validate and assess risk
                security_check = self.validator.validate_and_assess(intent, parameters)
                
                if not security_check['valid']:
                    print(f"{Fore.RED}{security_check['message']}{Style.RESET_ALL}")
                    print()
                    continue
                
                # Check if approval is required
                if security_check['requires_approval']:
                    # Display approval prompt
                    approval_prompt = self.validator.get_approval_prompt(
                        intent, parameters, security_check
                    )
                    print(approval_prompt)
                    
                    # Get user approval
                    approved, user_response = ApprovalPrompt.get_user_approval("")
                    
                    # Record decision
                    self.approval_manager.record_decision(
                        intent=intent,
                        parameters=parameters,
                        approved=approved,
                        risk_level=security_check['risk_level'],
                        user_response=user_response
                    )
                    
                    if not approved:
                        print(f"\n{Fore.YELLOW}Operation cancelled by user.{Style.RESET_ALL}\n")
                        
                        # Log cancelled operation
                        self.audit_logger.log_operation(
                            intent=intent.value,
                            parameters=parameters,
                            success=False,
                            risk_level=security_check['risk_level'].value,
                            approved=False,
                            result="Cancelled by user"
                        )
                        continue
                
                # Execute command
                print(f"{Fore.CYAN}⚙️  Processing...{Style.RESET_ALL}\n")
                
                result = self.router.route(intent_data)
                
                # Display result
                if result['success']:
                    print(f"{Fore.GREEN}{result['message']}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}{result['message']}{Style.RESET_ALL}")
                
                print()
                
                # Log operation
                self.audit_logger.log_operation(
                    intent=intent.value,
                    parameters=parameters,
                    success=result['success'],
                    risk_level=security_check['risk_level'].value if security_check['risk_level'] else None,
                    approved=security_check['requires_approval'] if security_check['requires_approval'] else None,
                    result=result['message'] if result['success'] else None,
                    error=result['message'] if not result['success'] else None
                )
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}Use 'exit' to quit KernelSense.{Style.RESET_ALL}\n")
                continue
            except Exception as e:
                print(f"\n{Fore.RED}❌ Unexpected error: {str(e)}{Style.RESET_ALL}\n")
                self.audit_logger.log_error(str(e))
                continue
        
        self.audit_logger.log_session_end()
    
    def _print_welcome(self):
        """Print welcome message"""
        print(f"{Fore.CYAN}{Style.BRIGHT}")
        print("Welcome to KernelSense!")
        print(f"{Style.RESET_ALL}")
        print("Ask me anything about your system in natural language.")
        print(f"Type {Fore.YELLOW}'help'{Style.RESET_ALL} for examples or {Fore.YELLOW}'exit'{Style.RESET_ALL} to quit.")
        print()
    
    def _get_user_input(self) -> str:
        """Get input from user"""
        try:
            prompt = f"{Fore.GREEN}You:{Style.RESET_ALL} "
            user_input = input(prompt).strip()
            return user_input
        except EOFError:
            return "exit"
    
    def _handle_exit(self):
        """Handle exit command"""
        print()
        print(f"{Fore.CYAN}Goodbye! 👋{Style.RESET_ALL}")
        
        # Show session statistics
        stats = self.audit_logger.get_statistics()
        
        if stats['total_operations'] > 0:
            print()
            print(f"{Fore.YELLOW}Session Summary:{Style.RESET_ALL}")
            print(f"  • Total operations: {stats['total_operations']}")
            print(f"  • Successful: {stats['successful_operations']}")
            print(f"  • Failed: {stats['failed_operations']}")
            
            if stats['operations_requiring_approval'] > 0:
                print(f"  • Operations requiring approval: {stats['operations_requiring_approval']}")
                print(f"    - Approved: {stats['approved_operations']}")
                print(f"    - Denied: {stats['denied_operations']}")
        
        print()
    
    def display_colored_message(self, message: str, color: str = "white"):
        """
        Display a colored message
        
        Args:
            message: Message to display
            color: Color name (green, red, yellow, cyan, white)
        """
        color_map = {
            'green': Fore.GREEN,
            'red': Fore.RED,
            'yellow': Fore.YELLOW,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE,
            'magenta': Fore.MAGENTA,
            'blue': Fore.BLUE
        }
        
        color_code = color_map.get(color.lower(), Fore.WHITE)
        print(f"{color_code}{message}{Style.RESET_ALL}")
