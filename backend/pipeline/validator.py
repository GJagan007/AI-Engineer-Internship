"""
Validation Engine
"""
import json
from typing import Dict, Any, List, Tuple
from models.schemas import ValidationResult
from utils.logger import logger


class Validator:
    """Validate generated output"""
    
    def validate_full(self, output: Dict[str, Any]) -> ValidationResult:
        """
        Validate complete output
        
        Args:
            output: Complete pipeline output
            
        Returns:
            ValidationResult
        """
        logger.info("Validating full output")
        errors = []
        warnings = []
        
        # Check required keys
        required_keys = ['intent', 'design', 'schemas']
        for key in required_keys:
            if key not in output:
                errors.append(f"Missing required key: {key}")
        
        if errors:
            return ValidationResult(valid=False, errors=errors, warnings=warnings)
        
        # Validate schemas
        schema_result = self.validate_schemas(output['schemas'])
        errors.extend(schema_result.errors)
        warnings.extend(schema_result.warnings)
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            needs_repair=len(errors) > 0 or len(warnings) > 0
        )
    
    def validate_schemas(self, schemas: Dict[str, Any]) -> ValidationResult:
        """Validate schemas"""
        errors = []
        warnings = []
        
        # Check schema keys
        required_keys = ['ui', 'api', 'db', 'auth']
        for key in required_keys:
            if key not in schemas:
                errors.append(f"Missing schema: {key}")
            elif not isinstance(schemas[key], dict):
                errors.append(f"Schema '{key}' must be an object")
        
        # Cross-layer validation
        if 'ui' in schemas and 'api' in schemas:
            self._validate_ui_api_consistency(schemas['ui'], schemas['api'], warnings)
        
        if 'db' in schemas and 'api' in schemas:
            self._validate_db_api_consistency(schemas['db'], schemas['api'], warnings)
        
        if 'auth' in schemas:
            self._validate_auth(schemas['auth'], warnings)
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            needs_repair=len(errors) > 0 or len(warnings) > 0
        )
    
    def _validate_ui_api_consistency(self, ui: Dict, api: Dict, warnings: List):
        """Validate UI to API consistency"""
        # Extract UI fields
        ui_fields = self._extract_ui_fields(ui)
        api_fields = self._extract_api_fields(api)
        
        for field in ui_fields:
            if field not in api_fields:
                warnings.append(f"UI field '{field}' not found in API")
    
    def _validate_db_api_consistency(self, db: Dict, api: Dict, warnings: List):
        """Validate DB to API consistency"""
        db_tables = self._extract_db_tables(db)
        api_resources = self._extract_api_resources(api)
        
        for table in db_tables:
            if table not in api_resources:
                warnings.append(f"DB table '{table}' has no API resource")
    
    def _validate_auth(self, auth: Dict, warnings: List):
        """Validate auth configuration"""
        if 'roles' not in auth:
            warnings.append("Auth missing roles definition")
        if 'permissions' not in auth:
            warnings.append("Auth missing permissions definition")
    
    def _extract_ui_fields(self, ui: Dict) -> List[str]:
        """Extract field names from UI schema"""
        fields = []
        schema_str = json.dumps(ui)
        import re
        matches = re.findall(r'"field":\s*"([^"]+)"', schema_str)
        return matches
    
    def _extract_api_fields(self, api: Dict) -> List[str]:
        """Extract field names from API schema"""
        fields = []
        schema_str = json.dumps(api)
        import re
        matches = re.findall(r'"field":\s*"([^"]+)"', schema_str)
        return matches
    
    def _extract_db_tables(self, db: Dict) -> List[str]:
        """Extract table names from DB schema"""
        tables = []
        if 'tables' in db:
            for table in db['tables']:
                if isinstance(table, dict) and 'name' in table:
                    tables.append(table['name'])
        return tables
    
    def _extract_api_resources(self, api: Dict) -> List[str]:
        """Extract resource names from API endpoints"""
        resources = []
        if 'endpoints' in api:
            for endpoint in api['endpoints']:
                if isinstance(endpoint, dict) and 'path' in endpoint:
                    parts = endpoint['path'].split('/')
                    if len(parts) > 1:
                        resources.append(parts[1])
        return resources