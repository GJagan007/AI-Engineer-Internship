"""
Custom Exceptions
"""


class PipelineError(Exception):
    """Base pipeline exception"""
    pass


class IntentExtractionError(PipelineError):
    """Failed to extract intent"""
    pass


class SystemDesignError(PipelineError):
    """Failed to design system"""
    pass


class SchemaGenerationError(PipelineError):
    """Failed to generate schemas"""
    pass


class ValidationError(PipelineError):
    """Validation failed"""
    pass


class RepairError(PipelineError):
    """Repair failed"""
    pass


class LLMServiceError(PipelineError):
    """LLM service error"""
    pass