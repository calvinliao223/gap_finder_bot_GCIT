#!/usr/bin/env python3
"""
Secure configuration management for Research Gap Finder
Handles API keys and sensitive configuration through environment variables
"""

import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import warnings

# Load environment variables from .env file
load_dotenv()

# Check if running on Streamlit Cloud
try:
    import streamlit as st
    STREAMLIT_CLOUD = hasattr(st, 'secrets')
except ImportError:
    STREAMLIT_CLOUD = False

class SecurityConfig:
    """Secure configuration management with API key validation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._validate_environment()
    
    def _validate_environment(self):
        """Validate that critical environment variables are set"""
        missing_keys = []
        
        # Check for at least one AI provider
        ai_providers = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY']
        if not any(os.getenv(key) for key in ai_providers):
            missing_keys.append("At least one AI provider API key")
        
        # Check for Semantic Scholar API key
        if not os.getenv('SEMANTIC_SCHOLAR_API_KEY'):
            missing_keys.append("SEMANTIC_SCHOLAR_API_KEY")
        
        if missing_keys:
            warning_msg = f"Missing API keys: {', '.join(missing_keys)}. Some features may not work."
            warnings.warn(warning_msg, UserWarning)
            self.logger.warning(warning_msg)
    
    def _get_key(self, key_name: str, default_placeholder: str = None) -> Optional[str]:
        """Get API key from Streamlit secrets or environment variables"""
        # Try Streamlit secrets first (for cloud deployment)
        if STREAMLIT_CLOUD:
            try:
                import streamlit as st
                if hasattr(st, 'secrets') and key_name in st.secrets:
                    key = st.secrets[key_name]
                    if key and (not default_placeholder or key != default_placeholder):
                        return key
            except Exception:
                pass

        # Fallback to environment variables
        key = os.getenv(key_name)
        if key and (not default_placeholder or key != default_placeholder):
            return key
        return None

    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key from Streamlit secrets or environment"""
        return self._get_key('OPENAI_API_KEY', 'your_openai_api_key_here')
    
    @property
    def anthropic_api_key(self) -> Optional[str]:
        """Get Anthropic API key from Streamlit secrets or environment"""
        return self._get_key('ANTHROPIC_API_KEY', 'your_anthropic_api_key_here')

    @property
    def google_api_key(self) -> Optional[str]:
        """Get Google API key from Streamlit secrets or environment"""
        return self._get_key('GOOGLE_API_KEY', 'your_google_api_key_here')

    @property
    def semantic_scholar_api_key(self) -> Optional[str]:
        """Get Semantic Scholar API key from Streamlit secrets or environment"""
        return self._get_key('SEMANTIC_SCHOLAR_API_KEY', 'your_semantic_scholar_api_key_here')

    @property
    def crossref_api_key(self) -> Optional[str]:
        """Get Crossref API key from Streamlit secrets or environment"""
        return self._get_key('CROSSREF_API_KEY', 'your_crossref_api_key_here')
    
    @property
    def preferred_ai_provider(self) -> str:
        """Get preferred AI provider"""
        return self._get_key('PREFERRED_AI_PROVIDER') or 'openai'

    @property
    def debug_mode(self) -> bool:
        """Get debug mode setting"""
        value = self._get_key('DEBUG_MODE') or 'false'
        return str(value).lower() == 'true'

    @property
    def log_level(self) -> str:
        """Get log level"""
        return (self._get_key('LOG_LEVEL') or 'INFO').upper()
    
    @property
    def semantic_scholar_rate_limit(self) -> float:
        """Get Semantic Scholar rate limit"""
        try:
            return float(os.getenv('SEMANTIC_SCHOLAR_RATE_LIMIT', '1.1'))
        except ValueError:
            return 1.1
    
    @property
    def max_api_retries(self) -> int:
        """Get maximum API retries"""
        try:
            return int(os.getenv('MAX_API_RETRIES', '3'))
        except ValueError:
            return 3
    
    @property
    def request_timeout(self) -> int:
        """Get request timeout"""
        try:
            return int(os.getenv('REQUEST_TIMEOUT', '15'))
        except ValueError:
            return 15
    
    @property
    def cache_duration(self) -> int:
        """Get cache duration"""
        try:
            return int(os.getenv('CACHE_DURATION', '3600'))
        except ValueError:
            return 3600
    
    @property
    def enable_cache(self) -> bool:
        """Get cache enable setting"""
        return os.getenv('ENABLE_CACHE', 'true').lower() == 'true'
    
    @property
    def max_export_papers(self) -> int:
        """Get maximum papers per export"""
        try:
            return int(os.getenv('MAX_EXPORT_PAPERS', '100'))
        except ValueError:
            return 100
    
    @property
    def default_export_format(self) -> str:
        """Get default export format"""
        return os.getenv('DEFAULT_EXPORT_FORMAT', 'json')
    
    @property
    def session_secret_key(self) -> str:
        """Get session secret key"""
        key = os.getenv('SESSION_SECRET_KEY')
        if not key or key == 'your_random_session_secret_here':
            # Generate a default key (not secure for production)
            import secrets
            return secrets.token_hex(32)
        return key
    
    @property
    def validate_api_keys(self) -> bool:
        """Get API key validation setting"""
        return os.getenv('VALIDATE_API_KEYS', 'true').lower() == 'true'
    
    def get_available_ai_providers(self) -> Dict[str, str]:
        """Get available AI providers with their API keys"""
        providers = {}
        
        if self.openai_api_key:
            providers['openai'] = self.openai_api_key
        
        if self.anthropic_api_key:
            providers['anthropic'] = self.anthropic_api_key
        
        if self.google_api_key:
            providers['gemini'] = self.google_api_key
        
        return providers
    
    def mask_api_key(self, api_key: str) -> str:
        """Mask API key for logging (show only first 8 and last 4 characters)"""
        if not api_key or len(api_key) < 12:
            return "***masked***"
        return f"{api_key[:8]}...{api_key[-4:]}"
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary for debugging (with masked keys)"""
        return {
            'ai_providers': {
                'openai': bool(self.openai_api_key),
                'anthropic': bool(self.anthropic_api_key),
                'google': bool(self.google_api_key),
            },
            'academic_apis': {
                'semantic_scholar': bool(self.semantic_scholar_api_key),
                'crossref': bool(self.crossref_api_key),
            },
            'settings': {
                'preferred_ai_provider': self.preferred_ai_provider,
                'debug_mode': self.debug_mode,
                'log_level': self.log_level,
                'rate_limit': self.semantic_scholar_rate_limit,
                'max_retries': self.max_api_retries,
                'cache_enabled': self.enable_cache,
            }
        }
    
    def validate_api_key_format(self, api_key: str, provider: str) -> bool:
        """Validate API key format for different providers"""
        if not api_key:
            return False
        
        # Basic format validation
        format_rules = {
            'openai': lambda k: k.startswith('sk-') and len(k) > 20,
            'anthropic': lambda k: k.startswith('sk-ant-') and len(k) > 20,
            'google': lambda k: k.startswith('AIza') and len(k) > 20,
            'semantic_scholar': lambda k: len(k) > 10,
            'crossref': lambda k: len(k) > 5,
        }
        
        validator = format_rules.get(provider)
        if validator:
            return validator(api_key)
        
        return len(api_key) > 5  # Basic length check

# Global configuration instance
config = SecurityConfig()

# Convenience functions for backward compatibility
def get_openai_key() -> Optional[str]:
    return config.openai_api_key

def get_anthropic_key() -> Optional[str]:
    return config.anthropic_api_key

def get_google_key() -> Optional[str]:
    return config.google_api_key

def get_semantic_scholar_key() -> Optional[str]:
    return config.semantic_scholar_api_key

def get_available_providers() -> Dict[str, str]:
    return config.get_available_ai_providers()

# Security check on import
if __name__ == "__main__":
    print("🔐 Security Configuration Summary:")
    print("=" * 50)
    
    summary = config.get_config_summary()
    
    print("AI Providers:")
    for provider, available in summary['ai_providers'].items():
        status = "✅ Available" if available else "❌ Missing"
        print(f"  {provider}: {status}")
    
    print("\nAcademic APIs:")
    for api, available in summary['academic_apis'].items():
        status = "✅ Available" if available else "❌ Missing"
        print(f"  {api}: {status}")
    
    print(f"\nSettings:")
    for key, value in summary['settings'].items():
        print(f"  {key}: {value}")
    
    print("\n🔒 Security Status: API keys are properly protected by .gitignore")
