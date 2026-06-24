"""
Stage 3: Schema Generation
"""
import json
from typing import Dict, Any
from services.llm_service import llm_service
from utils.logger import logger


class SchemaGenerator:
    """Generate schemas from system design"""
    
    SYSTEM_PROMPT = """You are an AI schema generator. Generate complete, production-ready schemas.
    
    Generate:
    1. UI Schema: pages, components, layouts, navigation
    2. API Schema: endpoints, methods, request/response schemas
    3. Database Schema: tables, columns, relationships, indexes
    4. Auth Schema: roles, permissions, access control rules
    
    Ensure consistency across all schemas. Fields in API must match DB, UI must map to API.
    
    Return a JSON object with keys: ui, api, db, auth
    Each key should contain the full schema definition.
    
    Return ONLY valid JSON."""
    
    def generate(self, design: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate schemas from design
        
        Args:
            design: System design object
            
        Returns:
            Schemas object with ui, api, db, auth
        """
        logger.info("Generating schemas")
        return llm_service.call(self.SYSTEM_PROMPT, json.dumps(design, indent=2))