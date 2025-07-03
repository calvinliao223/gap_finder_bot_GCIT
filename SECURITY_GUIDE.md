# 🔐 Security Guide - API Key Protection

## 🎯 **Overview**

This guide ensures your API keys and sensitive information are properly protected when using the Research Gap Finder. We've implemented comprehensive security measures to keep your credentials safe.

## 🚨 **CRITICAL: Never Commit API Keys to Git!**

**Your API keys are valuable and should be treated like passwords. Never commit them to version control.**

## 🔧 **Quick Setup**

### **1. Run Security Setup Script**
```bash
python setup_security.py
```

This interactive script will:
- Create your `.env` file
- Configure API keys securely
- Verify `.gitignore` protection
- Generate session secrets

### **2. Manual Setup (Alternative)**
```bash
# Copy template and edit
cp .env.template .env
# Edit .env with your real API keys
nano .env
```

## 📁 **Security Files**

### **✅ Protected Files (Never Committed)**
- **`.env`** - Your actual API keys and secrets
- **`.env.local`** - Local development overrides
- **`secrets.txt`** - Any additional secrets
- **`api_keys.txt`** - Alternative key storage
- **`credentials.json`** - Authentication files
- **`*.db`** - Database files with user data
- **`exports/`** - Research data exports
- **`cache/`** - Cached API responses

### **✅ Safe Files (Can Be Committed)**
- **`.env.template`** - Template with placeholder values
- **`.gitignore`** - Protection configuration
- **`config.py`** - Secure configuration loader
- **`setup_security.py`** - Security setup script
- **`SECURITY_GUIDE.md`** - This documentation

## 🔑 **API Key Configuration**

### **Required API Keys**

#### **1. AI Providers (Choose at least one)**
```bash
# OpenAI (GPT-4)
OPENAI_API_KEY=sk-proj-your-key-here

# Anthropic (Claude)
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# Google (Gemini)
GOOGLE_API_KEY=AIzaSy-your-key-here
```

#### **2. Academic Databases**
```bash
# Semantic Scholar (Required for paper search)
SEMANTIC_SCHOLAR_API_KEY=your-s2-key-here

# Crossref (Optional - enhances paper metadata)
CROSSREF_API_KEY=your-crossref-key-here
```

### **Where to Get API Keys**

| Provider | URL | Notes |
|----------|-----|-------|
| **OpenAI** | https://platform.openai.com/api-keys | Requires payment setup |
| **Anthropic** | https://console.anthropic.com/ | Claude API access |
| **Google** | https://makersuite.google.com/app/apikey | Free tier available |
| **Semantic Scholar** | https://www.semanticscholar.org/product/api | Free with registration |
| **Crossref** | https://www.crossref.org/services/metadata-delivery/rest-api/ | Optional enhancement |

## 🛡️ **Security Features**

### **1. Environment Variable Protection**
```python
# Secure configuration loading
from config import config

# API keys loaded securely
openai_key = config.openai_api_key  # None if not configured
semantic_key = config.semantic_scholar_api_key
```

### **2. API Key Validation**
```python
# Format validation for different providers
config.validate_api_key_format(key, 'openai')  # True/False
```

### **3. Key Masking for Logs**
```python
# Safe logging (shows only first 8 and last 4 characters)
masked_key = config.mask_api_key(api_key)  # "sk-proj12...xyz9"
```

### **4. Configuration Summary**
```python
# Get status without revealing keys
summary = config.get_config_summary()
# Returns: {'ai_providers': {'openai': True, 'anthropic': False}, ...}
```

## 🔒 **Best Practices**

### **✅ DO:**
- ✅ Use the `.env` file for API keys
- ✅ Keep `.env` in `.gitignore`
- ✅ Use strong, unique API keys
- ✅ Regularly rotate your keys
- ✅ Monitor API usage and costs
- ✅ Use the security setup script
- ✅ Validate key formats before use
- ✅ Keep backups of your `.env` file (securely)

### **❌ DON'T:**
- ❌ Commit API keys to version control
- ❌ Share API keys in chat/email
- ❌ Use API keys in URLs or logs
- ❌ Store keys in code files
- ❌ Use weak or default keys
- ❌ Ignore security warnings
- ❌ Share your `.env` file
- ❌ Use production keys in development

## 🔍 **Security Verification**

### **Check Your Setup**
```bash
# Run security verification
python setup_security.py
# Choose option 3: Verify security configuration
```

### **Manual Verification**
```bash
# Check .gitignore protection
grep -E "\.env|secrets|api_keys" .gitignore

# Verify .env exists but is not tracked
ls -la .env
git status .env  # Should show "not tracked"

# Test configuration loading
python -c "from config import config; print(config.get_config_summary())"
```

## 🚨 **Security Incidents**

### **If API Keys Are Compromised:**

1. **Immediate Actions:**
   ```bash
   # Revoke compromised keys immediately
   # - Go to provider's dashboard
   # - Revoke/delete the compromised key
   # - Generate new key
   ```

2. **Update Configuration:**
   ```bash
   # Update .env with new keys
   nano .env
   
   # Test new configuration
   python -c "from config import config; print('Keys loaded:', bool(config.openai_api_key))"
   ```

3. **Security Review:**
   ```bash
   # Check git history for leaked keys
   git log --all --full-history -- .env
   
   # If keys were committed, contact provider immediately
   ```

## 📊 **Security Monitoring**

### **Regular Security Checks**
```bash
# Weekly security verification
python setup_security.py  # Option 4: Show security status

# Monthly key rotation
# - Generate new API keys
# - Update .env file
# - Revoke old keys
```

### **API Usage Monitoring**
- Monitor API usage dashboards
- Set up billing alerts
- Review access logs regularly
- Watch for unusual activity patterns

## 🔧 **Troubleshooting**

### **Common Issues**

#### **"API key not found" Error**
```bash
# Check .env file exists
ls -la .env

# Verify key format
python -c "from config import config; print(config.get_config_summary())"

# Test specific provider
python -c "from config import config; print('OpenAI:', bool(config.openai_api_key))"
```

#### **"Secure config not available" Warning**
```bash
# Install missing dependency
pip install python-dotenv

# Verify config.py exists
ls -la config.py

# Test import
python -c "from config import config; print('Config loaded')"
```

#### **".env file not protected" Error**
```bash
# Check .gitignore
grep "\.env" .gitignore

# Add protection if missing
echo ".env" >> .gitignore
echo "*.env" >> .gitignore
```

## 🎯 **Security Checklist**

### **Initial Setup**
- [ ] ✅ `.env.template` copied to `.env`
- [ ] ✅ Real API keys configured in `.env`
- [ ] ✅ `.env` added to `.gitignore`
- [ ] ✅ `config.py` available and working
- [ ] ✅ Security setup script run successfully
- [ ] ✅ No API keys in code files
- [ ] ✅ Git status shows `.env` not tracked

### **Ongoing Security**
- [ ] ✅ Regular API key rotation (monthly)
- [ ] ✅ Monitor API usage and costs
- [ ] ✅ Review access logs
- [ ] ✅ Keep security tools updated
- [ ] ✅ Backup `.env` file securely
- [ ] ✅ Team members trained on security

## 🆘 **Emergency Contacts**

### **If Security Incident Occurs:**
1. **Revoke compromised keys immediately**
2. **Contact API providers' security teams**
3. **Review and update security measures**
4. **Document incident for future prevention**

### **Provider Security Contacts:**
- **OpenAI:** https://platform.openai.com/docs/guides/safety-best-practices
- **Anthropic:** https://console.anthropic.com/
- **Google:** https://cloud.google.com/security
- **Semantic Scholar:** https://www.semanticscholar.org/product/api

## 🎉 **Security Success**

**When properly configured, you'll have:**
- ✅ **Protected API keys** that never appear in version control
- ✅ **Secure configuration** with validation and error handling
- ✅ **Masked logging** that doesn't reveal sensitive data
- ✅ **Easy key management** with the setup script
- ✅ **Professional security** following industry best practices

**Your research data and API keys are now properly protected!** 🔒✨
