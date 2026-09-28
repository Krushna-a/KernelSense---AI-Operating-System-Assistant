"""
KernelSense - AI Operating-System Assistant
Main entry point for the application
"""

import sys
from cli.interface import KernelSenseCLI

def main():
    """Main entry point for KernelSense"""
    print("🧠 KernelSense - AI Operating-System Assistant")
    print("=" * 50)
    print()
    
    cli = KernelSenseCLI()
    cli.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 KernelSense shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
