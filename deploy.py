#!/usr/bin/env python3
"""
Deployment script for Yaswanth's AI Search Engine
Handles setup, testing, and deployment tasks
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def setup_virtual_environment():
    """Set up virtual environment"""
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("📁 Virtual environment already exists")
        return True
    
    return run_command("python -m venv .venv", "Creating virtual environment")

def install_dependencies():
    """Install project dependencies"""
    # Determine the correct pip path
    if os.name == 'nt':  # Windows
        pip_path = ".venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_path = ".venv/bin/pip"
    
    return run_command(f"{pip_path} install -r requirements.txt", "Installing dependencies")

def run_tests():
    """Run the test suite"""
    # Determine the correct python path
    if os.name == 'nt':  # Windows
        python_path = ".venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_path = ".venv/bin/python"
    
    return run_command(f"{python_path} -m pytest test_app.py -v", "Running tests")

def check_environment():
    """Check environment setup"""
    print("🔍 Checking environment setup...")
    
    # Check for .env file
    if not Path(".env").exists():
        print("⚠️  .env file not found. Creating template...")
        with open(".env", "w") as f:
            f.write("# Environment variables for Yaswanth's AI Search Engine\n")
            f.write("GROQ_API_KEY=your_groq_api_key_here\n")
        print("📝 Please edit .env file and add your Groq API key")
    
    # Check for required files
    required_files = ["app.py", "config.py", "utils.py", "requirements.txt"]
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ Environment setup looks good")
    return True

def start_application():
    """Start the Streamlit application"""
    # Determine the correct streamlit path
    if os.name == 'nt':  # Windows
        streamlit_path = ".venv\\Scripts\\streamlit"
    else:  # Unix/Linux/macOS
        streamlit_path = ".venv/bin/streamlit"
    
    print("🚀 Starting Yaswanth's AI Search Engine...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    
    try:
        subprocess.run(f"{streamlit_path} run app.py", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")

def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description="Deploy Yaswanth's AI Search Engine")
    parser.add_argument("--setup", action="store_true", help="Set up the environment")
    parser.add_argument("--test", action="store_true", help="Run tests")
    parser.add_argument("--start", action="store_true", help="Start the application")
    parser.add_argument("--all", action="store_true", help="Run setup, test, and start")
    
    args = parser.parse_args()
    
    print("🔍 Yaswanth's AI Search Engine - Deployment Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    success = True
    
    if args.setup or args.all:
        print("\n📦 Setting up environment...")
        success &= check_environment()
        success &= setup_virtual_environment()
        success &= install_dependencies()
    
    if args.test or args.all:
        print("\n🧪 Running tests...")
        success &= run_tests()
    
    if args.start or args.all:
        if success:
            print("\n🚀 Starting application...")
            start_application()
        else:
            print("❌ Cannot start application due to previous errors")
    
    if not any([args.setup, args.test, args.start, args.all]):
        print("ℹ️  No action specified. Use --help for available options")
        print("\nQuick start:")
        print("  python deploy.py --all    # Full setup and start")
        print("  python deploy.py --start  # Just start the app")

if __name__ == "__main__":
    main()
