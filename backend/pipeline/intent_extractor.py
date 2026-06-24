"""
Stage 1: Intent Extraction
"""
from typing import Dict, Any
from services.llm_service import llm_service
from utils.logger import logger


class IntentExtractor:
    """Extract structured intent from natural language"""
    
    SYSTEM_PROMPT = """You are an AI system that extracts structured intent from natural language requirements.
    
    Parse the user's request into a structured JSON with the following fields:
    - appType: The type of application (e.g., "crm", "ecommerce", "project-management", "social-media", "lms")
    - features: Array of key features mentioned
    - entities: Array of data entities (e.g., ["users", "contacts", "orders"])
    - roles: Array of user roles (e.g., ["admin", "user", "premium"])
    - auth: Authentication requirements (e.g., "email-password", "oauth")
    - payments: Payment requirements (e.g., "stripe", "paypal", null)
    - premium: Premium plan details (e.g., "subscription", "one-time", null)
    - complexity: "simple" | "moderate" | "complex"
    - confidence: 0-1 score of confidence in the extraction
    
    Return ONLY valid JSON."""
    
    def extract(self, prompt: str) -> Dict[str, Any]:
        """
        Extract intent from user prompt
        
        Args:
            prompt: User's natural language requirements
            
        Returns:
            Structured intent object
        """
        logger.info("Extracting intent from prompt")
        return llm_service.call(self.SYSTEM_PROMPT, prompt)