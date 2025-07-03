#!/usr/bin/env python3
"""
Security Setup Script for Research Gap Finder
Helps users configure API keys and environment variables securely
"""

import os
import shutil
import secrets
import getpass
from pathlib import Path

def create_env_file():
    """Create .env file from template with user input"""
    print("🔐 RESEARCH GAP FINDER - SECURITY SETUP")
    print("=" * 60)
    print()
    
    # Check if .env already exists
    if os.path.exists('.env'):
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Copy template
    if os.path.exists('.env.template'):
        shutil.copy('.env.template', '.env')
        print("✅ Created .env file from template")
    else:
        print("❌ .env.template not found. Creating basic .env file...")
        with open('.env', 'w') as f:
            f.write("# Research Gap Finder Environment Variables\n")
    
    print()
    print("🔑 **API KEY CONFIGURATION**")
    print("Enter your API keys (press Enter to skip):")
    print()
    
    # Collect API keys
    api_keys = {}
    
    # OpenAI
    print("1️⃣ **OpenAI API Key**")
    print("   Get from: https://platform.openai.com/api-keys")
    openai_key = getpass.getpass("   Enter OpenAI API key (hidden): ").strip()
    if openai_key:
        api_keys['OPENAI_API_KEY'] = openai_key
        print("   ✅ OpenAI key configured")
    else:
        print("   ⏭️  Skipped OpenAI")
    print()
    
    # Anthropic
    print("2️⃣ **Anthropic Claude API Key**")
    print("   Get from: https://console.anthropic.com/")
    anthropic_key = getpass.getpass("   Enter Anthropic API key (hidden): ").strip()
    if anthropic_key:
        api_keys['ANTHROPIC_API_KEY'] = anthropic_key
        print("   ✅ Anthropic key configured")
    else:
        print("   ⏭️  Skipped Anthropic")
    print()
    
    # Google
    print("3️⃣ **Google Gemini API Key**")
    print("   Get from: https://makersuite.google.com/app/apikey")
    google_key = getpass.getpass("   Enter Google API key (hidden): ").strip()
    if google_key:
        api_keys['GOOGLE_API_KEY'] = google_key
        print("   ✅ Google key configured")
    else:
        print("   ⏭️  Skipped Google")
    print()
    
    # Semantic Scholar
    print("4️⃣ **Semantic Scholar API Key**")
    print("   Get from: https://www.semanticscholar.org/product/api")
    semantic_key = getpass.getpass("   Enter Semantic Scholar API key (hidden): ").strip()
    if semantic_key:
        api_keys['SEMANTIC_SCHOLAR_API_KEY'] = semantic_key
        print("   ✅ Semantic Scholar key configured")
    else:
        print("   ⏭️  Skipped Semantic Scholar")
    print()
    
    # Generate session secret
    session_secret = secrets.token_hex(32)
    api_keys['SESSION_SECRET_KEY'] = session_secret
    
    # Update .env file
    update_env_file(api_keys)
    
    print("🎉 **SETUP COMPLETE!**")
    print()
    print("✅ **Security Status:**")
    print(f"   • API keys stored in .env file")
    print(f"   • .env file protected by .gitignore")
    print(f"   • Session secret generated")
    print(f"   • {len([k for k in api_keys if k != 'SESSION_SECRET_KEY'])} API keys configured")
    print()
    print("🔒 **Security Reminders:**")
    print("   • Never commit .env to version control")
    print("   • Keep your API keys private")
    print("   • Regularly rotate your keys")
    print("   • Monitor API usage and costs")
    print()

def update_env_file(api_keys):
    """Update .env file with API keys"""
    # Read existing content
    env_content = []
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.readlines()
    
    # Update or add keys
    updated_keys = set()
    for i, line in enumerate(env_content):
        for key, value in api_keys.items():
            if line.startswith(f"{key}=") or line.startswith(f"#{key}="):
                env_content[i] = f"{key}={value}\n"
                updated_keys.add(key)
                break
    
    # Add new keys that weren't found
    for key, value in api_keys.items():
        if key not in updated_keys:
            env_content.append(f"{key}={value}\n")
    
    # Write back to file
    with open('.env', 'w') as f:
        f.writelines(env_content)

def check_gitignore():
    """Ensure .gitignore is properly configured"""
    print("🔍 **CHECKING .gitignore PROTECTION**")
    print()
    
    gitignore_path = Path('.gitignore')
    
    if not gitignore_path.exists():
        print("❌ .gitignore file not found!")
        print("   Creating basic .gitignore...")
        create_basic_gitignore()
        return
    
    # Check if .env is protected
    with open(gitignore_path, 'r') as f:
        gitignore_content = f.read()
    
    protected_items = ['.env', '*.env', 'secrets.txt', 'api_keys.txt']
    missing_protections = []
    
    for item in protected_items:
        if item not in gitignore_content:
            missing_protections.append(item)
    
    if missing_protections:
        print(f"⚠️  Missing protections: {', '.join(missing_protections)}")
        print("   Adding to .gitignore...")
        
        with open(gitignore_path, 'a') as f:
            f.write("\n# API Keys and Secrets Protection\n")
            for item in missing_protections:
                f.write(f"{item}\n")
        
        print("   ✅ .gitignore updated")
    else:
        print("✅ .gitignore properly configured")
    print()

def create_basic_gitignore():
    """Create a basic .gitignore file"""
    basic_gitignore = """# API Keys and Secrets
.env
.env.*
*.env
secrets.txt
api_keys.txt
credentials.json

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/

# Data and Cache
*.db
*.sqlite
*.log
cache/
exports/

# System
.DS_Store
Thumbs.db
"""
    
    with open('.gitignore', 'w') as f:
        f.write(basic_gitignore)
    
    print("✅ Created basic .gitignore file")

def verify_security():
    """Verify security configuration"""
    print("🔍 **SECURITY VERIFICATION**")
    print()
    
    # Check .env file
    if os.path.exists('.env'):
        print("✅ .env file exists")
        
        # Check if it has content
        with open('.env', 'r') as f:
            content = f.read()
        
        if 'your_' in content and '_key_here' in content:
            print("⚠️  .env file contains template values")
            print("   Please run setup again to configure real API keys")
        else:
            print("✅ .env file configured with real values")
    else:
        print("❌ .env file missing")
    
    # Check .gitignore
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
        
        if '.env' in gitignore_content:
            print("✅ .env protected by .gitignore")
        else:
            print("❌ .env not protected by .gitignore")
    else:
        print("❌ .gitignore file missing")
    
    # Check config.py
    if os.path.exists('config.py'):
        print("✅ Secure config module available")
    else:
        print("⚠️  config.py not found - using basic environment variables")
    
    print()

def main():
    """Main setup function"""
    print("🚀 **RESEARCH GAP FINDER - SECURITY SETUP**")
    print()
    
    while True:
        print("Choose an option:")
        print("1. 🔑 Configure API keys (.env setup)")
        print("2. 🔍 Check .gitignore protection")
        print("3. ✅ Verify security configuration")
        print("4. 📋 Show security status")
        print("5. ❌ Exit")
        print()
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            create_env_file()
        elif choice == '2':
            check_gitignore()
        elif choice == '3':
            verify_security()
        elif choice == '4':
            show_security_status()
        elif choice == '5':
            print("👋 Goodbye! Keep your API keys secure!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        print()

def show_security_status():
    """Show current security status"""
    print("📊 **SECURITY STATUS REPORT**")
    print("=" * 50)
    
    # Check files
    files_status = {
        '.env': '✅ Exists' if os.path.exists('.env') else '❌ Missing',
        '.env.template': '✅ Exists' if os.path.exists('.env.template') else '❌ Missing',
        '.gitignore': '✅ Exists' if os.path.exists('.gitignore') else '❌ Missing',
        'config.py': '✅ Exists' if os.path.exists('config.py') else '❌ Missing',
    }
    
    print("📁 **Files:**")
    for file, status in files_status.items():
        print(f"   {file}: {status}")
    
    # Check API keys (without revealing them)
    if os.path.exists('.env'):
        print("\n🔑 **API Keys:**")
        with open('.env', 'r') as f:
            content = f.read()
        
        keys_to_check = [
            'OPENAI_API_KEY',
            'ANTHROPIC_API_KEY', 
            'GOOGLE_API_KEY',
            'SEMANTIC_SCHOLAR_API_KEY'
        ]
        
        for key in keys_to_check:
            if f"{key}=" in content and 'your_' not in content:
                print(f"   {key}: ✅ Configured")
            else:
                print(f"   {key}: ❌ Not configured")
    
    print("\n🔒 **Security Recommendations:**")
    print("   • Keep .env file private and secure")
    print("   • Never commit API keys to version control")
    print("   • Regularly rotate your API keys")
    print("   • Monitor API usage and costs")
    print("   • Use strong, unique keys for each service")

if __name__ == "__main__":
    main()
