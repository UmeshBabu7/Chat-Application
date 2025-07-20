#!/usr/bin/env python3
"""
Test script to verify the Chat Application setup
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        from app.config import settings
        print("✓ Config imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import config: {e}")
        return False
    
    try:
        from app.database import engine, get_db
        print("✓ Database module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import database: {e}")
        return False
    
    try:
        from app.models import Base, User, Message, UserRole
        print("✓ Models imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import models: {e}")
        return False
    
    try:
        from app.auth import create_access_token, verify_token
        print("✓ Auth module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import auth: {e}")
        return False
    
    try:
        from app.crud import create_user, get_user_by_username
        print("✓ CRUD module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import CRUD: {e}")
        return False
    
    return True

def test_database_connection():
    """Test database connection."""
    print("\nTesting database connection...")
    
    try:
        from app.database import engine
        from app.models import Base
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✓ Database connection successful")
        
        # Test table creation
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
        
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("Make sure PostgreSQL is running and DATABASE_URL is correct in .env file")
        return False

def test_config():
    """Test configuration settings."""
    print("\nTesting configuration...")
    
    try:
        from app.config import settings
        
        print(f"✓ Database URL: {settings.DATABASE_URL}")
        print(f"✓ Secret Key: {'*' * len(settings.SECRET_KEY)}")
        print(f"✓ Algorithm: {settings.ALGORITHM}")
        print(f"✓ Token Expire Minutes: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
        print(f"✓ Debug Mode: {settings.DEBUG}")
        print(f"✓ Host: {settings.HOST}")
        print(f"✓ Port: {settings.PORT}")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Chat Application Setup Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Check your dependencies.")
        sys.exit(1)
    
    # Test configuration
    if not test_config():
        print("\n❌ Configuration test failed. Check your .env file.")
        sys.exit(1)
    
    # Test database connection
    if not test_database_connection():
        print("\n❌ Database connection failed. Check your PostgreSQL setup.")
        sys.exit(1)
    
    print("\n✅ All tests passed! Your Chat Application is ready to run.")
    print("\nTo start the application, run:")
    print("  python run.py")
    print("  or")
    print("  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main() 