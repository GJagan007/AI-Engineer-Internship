"""
Stage 4: Refinement Engine - Validation and Repair
"""
import json
import re
from typing import Dict, Any, List
from models.schemas import ValidationResult
from services.llm_service import llm_service
from utils.logger import logger


class RefinementEngine:
    """Validate and repair schemas"""
    
    SYSTEM_PROMPT = """You are an AI refinement engine. Validate and repair cross-layer inconsistencies.
    
    Check for:
    1. API fields match DB schema
    2. UI fields map to API endpoints
    3. Auth rules cover all entities and endpoints
    4. No missing required fields
    5. Consistent naming conventions
    
    Fix any issues automatically and return the repaired schemas.
    If issues cannot be repaired, document them in an "issues" field.
    
    Return the complete schemas object with any repairs applied."""
    
    def validate(self, schemas: Dict[str, Any]) -> ValidationResult:
        """
        Validate schemas for consistency
        
        Args:
            schemas: Generated schemas
            
        Returns:
            ValidationResult with errors and warnings
        """
        logger.info("Validating schemas")
        errors = []
        warnings = []
        
        # Check required keys
        required_keys = ['ui', 'api', 'db', 'auth']
        for key in required_keys:
            if key not in schemas:
                errors.append(f"Missing required schema: {key}")
        
        # Cross-layer consistency
        if 'ui' in schemas and 'api' in schemas:
            ui_fields = self._extract_fields(schemas['ui'])
            api_fields = self._extract_api_fields(schemas['api'])
            for field in ui_fields:
                if field not in api_fields:
                    warnings.append(f"UI field '{field}' not mapped to API")
        
        if 'db' in schemas and 'api' in schemas:
            db_tables = self._extract_tables(schemas['db'])
            api_endpoints = self._extract_endpoints(schemas['api'])
            for table in db_tables:
                if table not in api_endpoints:
                    warnings.append(f"DB table '{table}' has no API endpoint")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            needs_repair=len(errors) > 0 or len(warnings) > 0
        )
    
    def repair(self, schemas: Dict[str, Any], intent: Dict[str, Any], design: Dict[str, Any]) -> Dict[str, Any]:
        """
        Repair schemas using LLM
        
        Args:
            schemas: Schemas to repair
            intent: Original intent
            design: System design
            
        Returns:
            Repaired schemas
        """
        logger.info("Repairing schemas")
        context = {
            "intent": intent,
            "design": design,
            "schemas": schemas
        }
        result = llm_service.call(self.SYSTEM_PROMPT, json.dumps(context, indent=2))
        
        # Add repair metadata
        result['_repaired'] = True
        result['_repair_timestamp'] = str(intent)  # Simple tracking
        
        return result
    
    def _extract_fields(self, ui_schema: Dict) -> list:
        """Extract field names from UI schema"""
        fields = []
        schema_str = json.dumps(ui_schema)
        matches = re.findall(r'"field":\s*"([^"]+)"', schema_str)
        return matches
    
    def _extract_api_fields(self, api_schema: Dict) -> list:
        """Extract field names from API schema"""
        fields = []
        schema_str = json.dumps(api_schema)
        matches = re.findall(r'"field":\s*"([^"]+)"', schema_str)
        return matches
    
    def _extract_tables(self, db_schema: Dict) -> list:
        """Extract table names from DB schema"""
        tables = []
        if 'tables' in db_schema:
            for table in db_schema['tables']:
                if isinstance(table, dict) and 'name' in table:
                    tables.append(table['name'])
        return tables
    
    def _extract_endpoints(self, api_schema: Dict) -> list:
        """Extract endpoint names from API schema"""
        endpoints = []
        if 'endpoints' in api_schema:
            for endpoint in api_schema['endpoints']:
                path = endpoint.get('path', '')
                # Extract resource name from path
                parts = path.split('/')
                if len(parts) > 1:
                    endpoints.append(parts[1])
        return endpoints