"""
Stage 2: System Design
"""
import json
from typing import Dict, Any
from services.llm_service import llm_service
from utils.logger import logger


class SystemDesigner:
    """Design system architecture from intent"""
    
    SYSTEM_PROMPT = """You are an AI system architect. Design the application architecture based on the extracted intent.
    
    Generate a structured system design with:
    - entities: Array of entity definitions with name, fields, relations
    - flows: Array of user flows (e.g., ["login", "signup", "create-contact"])
    - roles: Array of role definitions with permissions
    - modules: Array of module names
    - architecture: "monolithic" | "microservices" | "serverless"
    - database: "postgres" | "mongodb" | "mysql" | "sqlite"
    
    Return ONLY valid JSON."""
    
    def design(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Design system from intent
        
        Args:
            intent: Extracted intent object
            
        Returns:
            System design object
        """
        logger.info("Designing system architecture")
        return llm_service.call(self.SYSTEM_PROMPT, json.dumps(intent, indent=2))