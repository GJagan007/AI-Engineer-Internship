"""
Configuration Management
"""
import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


@dataclass
class Config:
    """Application configuration"""
    
    # OpenAI Configuration - Force mock mode
    openai_api_key: str = ''  # Empty = mock mode
    openai_model: str = 'gpt-4-turbo-preview'
    openai_temperature: float = 0.3
    openai_max_tokens: int = 4000
    
    # Server Configuration
    port: int = int(os.getenv('PORT', '5000'))
    debug: bool = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Pipeline Configuration
    max_retries: int = 3
    repair_attempts: int = 2
    timeout_ms: int = 60000
    
    # Feature Flags
    enable_validation: bool = True
    enable_repair: bool = True
    enable_execution: bool = True
    
    @property
    def has_openai_key(self) -> bool:
        return False  # Force mock mode


config = Config()