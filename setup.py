"""
Setup script for KernelSense
Checks dependencies and prepares the environment
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def verify_imports():
    """Verify that all required modules can be imported"""
    print("\n🔍 Verifying imports...")
    required_modules = [
        ('psutil', 'System information library'),
        ('colorama', 'Colored terminal output')
    ]
    
    all_ok = True
    for module, description in required_modules:
        try:
            __import__(module)
            print(f"✓ {module} - {description}")
        except ImportError:
            print(f"❌ {module} - Not found")
            all_ok = False
    
    return all_ok

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    directories = ['logs']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created {directory}/")
        else:
            print(f"✓ {directory}/ already exists")
    
    return True

def verify_modules():
    """Verify that KernelSense modules are present"""
    print("\n🔍 Verifying KernelSense modules...")
    modules = [
        'cli/interface.py',
        'core/intent_parser.py',
        'core/command_router.py',
        'core/operations.py',
        'core/audit_logger.py',
        'security/risk_assessor.py',
        'security/validator.py',
        'security/approval_manager.py',
        'system_info/collector.py',
        'system_info/formatters.py'
    ]
    
    all_ok = True
    for module in modules:
        if os.path.exists(module):
            print(f"✓ {module}")
        else:
            print(f"❌ {module} - Missing!")
            all_ok = False
    
    return all_ok

def test_import():
    """Test importing the main module"""
    print("\n🧪 Testing KernelSense import...")
    try:
        from cli.interface import KernelSenseCLI
        print("✓ KernelSense imports successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("🧠 KernelSense Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Verify modules
    if not verify_modules():
        print("\n❌ Some KernelSense modules are missing!")
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Verify imports
    if not verify_imports():
        print("\n❌ Some dependencies failed to import")
        print("   Try: pip install -r requirements.txt")
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Test import
    if not test_import():
        return False
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("=" * 60)
    print("\n🚀 You can now run KernelSense:")
    print("   python kernelsense.py")
    print("\n📚 Documentation:")
    print("   - README.md - Complete documentation")
    print("   - QUICKSTART.md - Quick start guide")
    print("   - EXAMPLES.md - Usage examples")
    print("   - ARCHITECTURE.md - Technical details")
    print()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
