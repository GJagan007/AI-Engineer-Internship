"""
Execution Service - Simulate application execution
"""
import json
import re
from typing import Dict, Any
from utils.logger import logger


class ExecutionService:
    """Service to simulate application execution"""
    
    def execute(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate execution of generated application
        
        Args:
            config: Complete application configuration
            
        Returns:
            Execution results
        """
        logger.info("Simulating application execution")
        
        results = []
        success = True
        
        # Phase 1: Validate configuration
        try:
            self._validate_config(config)
            results.append({
                'phase': 'validation',
                'status': 'success',
                'message': 'Configuration validation passed'
            })
        except Exception as e:
            results.append({
                'phase': 'validation',
                'status': 'error',
                'message': str(e)
            })
            success = False
        
        # Phase 2: Check cross-layer consistency
        try:
            consistency = self._check_consistency(config)
            results.append({
                'phase': 'consistency',
                'status': 'success' if consistency['passed'] else 'warning',
                'message': consistency['message'],
                'details': consistency['details']
            })
        except Exception as e:
            results.append({
                'phase': 'consistency',
                'status': 'error',
                'message': str(e)
            })
            success = False
        
        # Phase 3: Generate runtime
        try:
            runtime = self._generate_runtime(config)
            results.append({
                'phase': 'runtime-generation',
                'status': 'success',
                'message': f"Generated {runtime['files']} files",
                'details': runtime
            })
        except Exception as e:
            results.append({
                'phase': 'runtime-generation',
                'status': 'error',
                'message': str(e)
            })
            success = False
        
        # Phase 4: Simulate execution
        try:
            execution = self._simulate_execution(config)
            results.append({
                'phase': 'execution-simulation',
                'status': 'success' if execution['success'] else 'error',
                'message': execution['message'],
                'details': execution['details']
            })
        except Exception as e:
            results.append({
                'phase': 'execution-simulation',
                'status': 'error',
                'message': str(e)
            })
            success = False
        
        return {
            'success': success,
            'results': results,
            'summary': {
                'total_phases': len(results),
                'successful_phases': sum(1 for r in results if r['status'] != 'error'),
                'failed_phases': sum(1 for r in results if r['status'] == 'error')
            }
        }
    
    def _validate_config(self, config: Dict[str, Any]):
        """Validate configuration"""
        required = ['intent', 'design', 'schemas']
        for key in required:
            if key not in config:
                raise ValueError(f"Missing required config key: {key}")
    
    def _check_consistency(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Check cross-layer consistency"""
        details = []
        passed = True
        
        schemas = config.get('schemas', {})
        design = config.get('design', {})
        
        # Check UI to API
        if 'ui' in schemas and 'api' in schemas:
            ui_fields = self._extract_ui_fields(schemas['ui'])
            api_fields = self._extract_api_fields(schemas['api'])
            mapped = [f for f in ui_fields if f in api_fields]
            details.append(f"UI fields mapped to API: {len(mapped)}/{len(ui_fields)}")
            if len(mapped) < len(ui_fields):
                passed = False
                details.append(f"Warning: {len(ui_fields) - len(mapped)} UI fields not mapped")
        
        # Check DB to API
        if 'db' in schemas and 'api' in schemas:
            db_tables = self._extract_db_tables(schemas['db'])
            api_resources = self._extract_api_resources(schemas['api'])
            details.append(f"DB tables mapped to API: {len(db_tables)}/{len(api_resources)}")
        
        return {
            'passed': passed,
            'message': 'Cross-layer consistency verified' if passed else 'Cross-layer inconsistencies found',
            'details': details
        }
    
    def _generate_runtime(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate runtime files"""
        files = ['app.js', 'routes.js', 'models.js', 'auth.js', 'ui.js']
        return {
            'files': len(files),
            'file_list': files,
            'structure': 'src/',
            'dependencies': ['express', 'react', 'postgresql']
        }
    
    def _simulate_execution(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate application execution"""
        return {
            'success': True,
            'message': 'Application started successfully',
            'details': {
                'port': 3000,
                'status': 'running',
                'url': 'http://localhost:3000',
                'routes_count': 12,
                'models_count': 6
            }
        }
    
    def _extract_ui_fields(self, ui: Dict) -> list:
        """Extract UI fields"""
        fields = []
        schema_str = json.dumps(ui)
        matches = re.findall(r'"field":\s*"([^"]+)"', schema_str)
        return matches
    
    def _extract_api_fields(self, api: Dict) -> list:
        """Extract API fields"""
        fields = []
        schema_str = json.dumps(api)
        matches = re.findall(r'"field":\s*"([^"]+)"', schema_str)
        return matches
    
    def _extract_db_tables(self, db: Dict) -> list:
        """Extract DB tables"""
        tables = []
        if 'tables' in db:
            for table in db['tables']:
                if isinstance(table, dict) and 'name' in table:
                    tables.append(table['name'])
        return tables
    
    def _extract_api_resources(self, api: Dict) -> list:
        """Extract API resources"""
        resources = []
        if 'endpoints' in api:
            for endpoint in api['endpoints']:
                if isinstance(endpoint, dict) and 'path' in endpoint:
                    parts = endpoint['path'].split('/')
                    if len(parts) > 1:
                        resources.append(parts[1])
        return resources