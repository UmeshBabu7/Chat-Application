#!/usr/bin/env python3
"""
Setup script for the Chat Application
"""
import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"✗ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_virtual_environment():
    """Create a virtual environment."""
    if os.path.exists("venv"):
        print("✓ Virtual environment already exists")
        return True
    
    return run_command("python -m venv venv", "Creating virtual environment")

def install_dependencies():
    """Install Python dependencies."""
    # Determine the correct pip command
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")

def create_env_file():
    """Create .env file from template."""
    if os.path.exists(".env"):
        print("✓ .env file already exists")
        return True
    
    if os.path.exists("env.example"):
        shutil.copy("env.example", ".env")
        print("✓ Created .env file from template")
        print("⚠️  Please update .env file with your database credentials")
        return True
    else:
        print("✗ env.example file not found")
        return False

def initialize_alembic():
    """Initialize Alembic for database migrations."""
    if os.path.exists("alembic.ini"):
        print("✓ Alembic already initialized")
        return True
    
    return run_command("alembic init alembic", "Initializing Alembic")

def main():
    """Main setup function."""
    print("Chat Application Setup")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("\n❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("\n❌ Failed to create .env file")
        sys.exit(1)
    
    # Initialize Alembic
    if not initialize_alembic():
        print("\n❌ Failed to initialize Alembic")
        sys.exit(1)
    
    print("\n✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Update .env file with your database credentials")
    print("2. Create a PostgreSQL database named 'chat_app'")
    print("3. Run: python test_setup.py")
    print("4. Run: python run.py")
    print("\nFor detailed instructions, see README.md")

if __name__ == "__main__":
    main() 