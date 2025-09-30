#!/usr/bin/env python3
"""
Setup script for the Regulatory Report Assistant Django backend
"""
import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def setup_django():
    """Setup Django project"""
    print("🚀 Setting up Regulatory Report Assistant Django Backend")
    print("=" * 60)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'regulatory_assistant.settings')
    
    try:
        django.setup()
        print("✅ Django setup completed")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False
    
    return True

def run_migrations():
    """Run Django migrations"""
    print("\n🔄 Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Database migrations completed")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_superuser():
    """Create Django superuser"""
    print("\n🔄 Creating superuser...")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@gmail.com', 'admin123')
            print("✅ Superuser created (username: admin, password: admin123)")
        else:
            print("ℹ️  Superuser already exists")
        return True
    except Exception as e:
        print(f"❌ Superuser creation failed: {e}")
        return False

def install_spacy_model():
    """Install spaCy English model"""
    print("\n🔄 Installing spaCy English model...")
    try:
        # If already installed and loadable, skip reinstall
        import spacy
        try:
            spacy.load('en_core_web_sm')
            print("✅ spaCy model already installed and loadable")
            return True
        except Exception:
            pass

        # Attempt standard downloader first
        try:
            subprocess.run([sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'], 
                          check=True)
        except subprocess.CalledProcessError as e:
            print("⚠️  spaCy downloader failed, trying direct wheel install for en_core_web_sm==3.7.1 ...")
            # Fallback to exact wheel compatible with spaCy 3.7.x
            wheel_url = (
                'https://github.com/explosion/spacy-models/releases/download/'
                'en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl'
            )
            subprocess.run([sys.executable, '-m', 'pip', 'install', wheel_url], check=True)

        # Verify load
        try:
            spacy.load('en_core_web_sm')
            print("✅ spaCy model installed and verified")
            return True
        except Exception as e:
            print(f"❌ spaCy model installation appears to have failed: {e}")
            print("ℹ️  The app will continue using fallback regex patterns.")
            return True  # Not critical for basic functionality
    except Exception as e:
        print(f"⚠️  spaCy model step encountered an unexpected error: {e}")
        print("ℹ️  The app will continue using fallback regex patterns.")
        return True

def main():
    """Main setup function"""
    success = True
    
    # Setup Django
    if not setup_django():
        success = False
    
    # Run migrations
    if not run_migrations():
        success = False
    
    # Create superuser
    if not create_superuser():
        success = False
    
    # Install spaCy model
    if not install_spacy_model():
        success = False
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("\nTo start the server, run:")
        print("  python manage.py runserver")
        print("\nThe API will be available at: http://localhost:8000")
        print("Admin interface at: http://localhost:8000/admin")
        print("API documentation at: http://localhost:8000/api/")
    else:
        print("\n❌ Setup completed with errors. Please check the messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
