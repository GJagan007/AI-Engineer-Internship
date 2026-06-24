"""
Pipeline Orchestrator - Main Compilation Pipeline
"""
import time
from typing import Dict, Any
from models.metrics import PipelineMetrics
from pipeline.intent_extractor import IntentExtractor
from pipeline.system_designer import SystemDesigner
from pipeline.schema_generator import SchemaGenerator
from pipeline.refinement_engine import RefinementEngine
from pipeline.validator import Validator
from services.execution_service import ExecutionService
from utils.logger import logger


class PipelineOrchestrator:
    """Orchestrate the multi-stage compilation pipeline"""
    
    def __init__(self):
        self.intent_extractor = IntentExtractor()
        self.system_designer = SystemDesigner()
        self.schema_generator = SchemaGenerator()
        self.refinement_engine = RefinementEngine()
        self.validator = Validator()
        self.execution_service = ExecutionService()
        self.metrics = PipelineMetrics()
        
    def compile(self, prompt: str) -> Dict[str, Any]:
        """Main compilation pipeline"""
        start_time = time.time()
        self.metrics.total_requests += 1
        
        try:
            logger.info("Stage 1: Extracting intent...")
            intent = self.intent_extractor.extract(prompt)
            
            logger.info("Stage 2: Designing system...")
            design = self.system_designer.design(intent)
            
            logger.info("Stage 3: Generating schemas...")
            schemas = self.schema_generator.generate(design)
            
            logger.info("Stage 4: Validating schemas...")
            validation_result = self.refinement_engine.validate(schemas)
            
            if validation_result.needs_repair:
                logger.info("Stage 5: Repairing schemas...")
                schemas = self.refinement_engine.repair(schemas, intent, design)
                self.metrics.total_repairs += 1
                validation_result = self.refinement_engine.validate(schemas)
            
            logger.info("Stage 6: Executing application...")
            execution_result = self.execution_service.execute({
                'intent': intent,
                'design': design,
                'schemas': schemas
            })
            
            total_time = time.time() - start_time
            self.metrics.success_count += 1
            self.metrics.total_latency += total_time
            self.metrics.latency_history.append(total_time)
            
            result = {
                'intent': intent,
                'design': design,
                'schemas': schemas,
                'validation': {
                    'valid': validation_result.valid,
                    'errors': validation_result.errors,
                    'warnings': validation_result.warnings,
                    'needs_repair': validation_result.needs_repair
                },
                'execution': execution_result,
                'metadata': {
                    'total_time_ms': total_time * 1000,
                    'success': True,
                    'repaired': validation_result.needs_repair,
                    'version': '1.0.0',
                    'mode': 'mock'
                }
            }
            
            logger.info(f"Compilation successful in {total_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Compilation failed: {e}")
            self.metrics.failure_count += 1
            
            return {
                'error': str(e),
                'metadata': {
                    'total_time_ms': (time.time() - start_time) * 1000,
                    'success': False,
                    'version': '1.0.0',
                    'mode': 'mock'
                }
            }
    
    def get_metrics(self) -> Dict[str, Any]:
        return self.metrics.to_dict()


pipeline = PipelineOrchestrator()