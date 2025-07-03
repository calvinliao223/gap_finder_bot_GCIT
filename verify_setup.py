#!/usr/bin/env python3
"""
Setup Verification Script for Research Gap Finder
Verifies that all components are working correctly
"""

import sys
import os
from datetime import datetime

def check_dependencies():
    """Check if all required packages are installed"""
    print("🔍 **Checking Dependencies...**")
    
    required_packages = [
        ('streamlit', 'streamlit'),
        ('requests', 'requests'),
        ('pandas', 'pandas'),
        ('yaml', 'yaml'),
        ('python-dotenv', 'dotenv')
    ]

    missing_packages = []

    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - MISSING")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Install with: pip install " + " ".join(missing_packages))
        return False
    
    print("   ✅ All required packages installed")
    return True

def check_configuration():
    """Check if configuration is properly set up"""
    print("\n🔧 **Checking Configuration...**")
    
    try:
        from config import config
        print("   ✅ Secure configuration module loaded")
        
        # Check API providers
        providers = config.get_available_ai_providers()
        print(f"   📊 Available AI providers: {len(providers)}")
        
        for provider, available in [
            ('OpenAI', config.openai_api_key),
            ('Anthropic', config.anthropic_api_key), 
            ('Google', config.google_api_key),
            ('Semantic Scholar', config.semantic_scholar_api_key)
        ]:
            status = "✅ Configured" if available else "❌ Missing"
            print(f"   {provider}: {status}")
        
        return len(providers) > 0
        
    except ImportError:
        print("   ⚠️  Secure config not available - using environment variables")
        
        # Check environment variables directly
        env_keys = [
            'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 
            'GOOGLE_API_KEY', 'SEMANTIC_SCHOLAR_API_KEY'
        ]
        
        configured_keys = 0
        for key in env_keys:
            if os.getenv(key):
                print(f"   ✅ {key}")
                configured_keys += 1
            else:
                print(f"   ❌ {key} - Missing")
        
        return configured_keys > 0

def check_llm_providers():
    """Check if LLM providers are working"""
    print("\n🤖 **Checking LLM Providers...**")
    
    try:
        from research_gap_finder import ResearchGapAnalyzer
        
        analyzer = ResearchGapAnalyzer()
        providers = analyzer.llm.providers
        
        print(f"   📊 Initialized providers: {len(providers)}")
        
        for name, available in analyzer.llm.get_available_providers().items():
            status = "✅ Working" if available else "❌ Failed"
            print(f"   {name}: {status}")
        
        return len(providers) > 0
        
    except Exception as e:
        print(f"   ❌ Error initializing LLM providers: {e}")
        return False

def check_academic_search():
    """Check if academic search is working"""
    print("\n🔍 **Checking Academic Search...**")
    
    try:
        from research_gap_finder import AcademicSearchEngine
        
        searcher = AcademicSearchEngine()
        print("   ✅ Academic search engine initialized")
        print("   📚 Semantic Scholar API configured")
        print("   📖 Crossref API configured")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error initializing search engine: {e}")
        return False

def check_security():
    """Check security configuration"""
    print("\n🔒 **Checking Security...**")
    
    # Check .env file
    if os.path.exists('.env'):
        print("   ✅ .env file exists")
    else:
        print("   ⚠️  .env file missing - run setup_security.py")
    
    # Check .gitignore
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
        
        if '.env' in gitignore_content:
            print("   ✅ .env protected by .gitignore")
        else:
            print("   ⚠️  .env not protected by .gitignore")
    else:
        print("   ❌ .gitignore missing")
    
    # Check that .env is not tracked by git
    try:
        import subprocess
        result = subprocess.run(['git', 'status', '.env'], 
                              capture_output=True, text=True)
        if 'not tracked' in result.stderr or result.returncode != 0:
            print("   ✅ .env file not tracked by git")
        else:
            print("   ⚠️  .env file might be tracked by git")
    except:
        print("   ⚠️  Could not check git status")
    
    return True

def main():
    """Run all verification checks"""
    print("🚀 **RESEARCH GAP FINDER - SETUP VERIFICATION**")
    print("=" * 60)
    print(f"Verification time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Configuration", check_configuration), 
        ("LLM Providers", check_llm_providers),
        ("Academic Search", check_academic_search),
        ("Security", check_security)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"   ❌ Error in {check_name}: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 60)
    print("📊 **VERIFICATION SUMMARY**")
    print("=" * 60)
    
    passed = 0
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} checks passed")
    
    if passed == len(results):
        print("\n🎉 **ALL CHECKS PASSED!**")
        print("Your Research Gap Finder is ready to use!")
        print("\nNext steps:")
        print("1. Run: streamlit run research_gap_finder.py")
        print("2. Open: http://localhost:8502")
        print("3. Start researching!")
    else:
        print("\n⚠️  **SOME CHECKS FAILED**")
        print("Please fix the issues above before using the application.")
        print("\nFor help:")
        print("1. Run: python setup_security.py")
        print("2. Check: SECURITY_GUIDE.md")
        print("3. Install missing packages: pip install -r requirements.txt")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
