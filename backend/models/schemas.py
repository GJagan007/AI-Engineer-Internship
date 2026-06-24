"""
Pydantic Models for Data Validation
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class IntentExtraction:
    """Extracted intent from user prompt"""
    appType: str
    features: List[str]
    entities: List[str]
    roles: List[str]
    auth: str
    complexity: str
    confidence: float
    payments: Optional[str] = None
    premium: Optional[str] = None


@dataclass
class SystemDesign:
    """System architecture design"""
    entities: List[Dict[str, Any]]
    flows: List[str]
    roles: List[Dict[str, Any]]
    modules: List[str]
    architecture: str
    database: str


@dataclass
class Schemas:
    """Generated schemas"""
    ui: Dict[str, Any]
    api: Dict[str, Any]
    db: Dict[str, Any]
    auth: Dict[str, Any]


@dataclass
class ValidationResult:
    """Validation results"""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    needs_repair: bool = False


@dataclass
class CompileRequest:
    """Compile request model"""
    prompt: str


@dataclass
class CompileResponse:
    """Compile response model"""
    intent: IntentExtraction
    design: SystemDesign
    schemas: Schemas
    validation: ValidationResult
    metadata: Dict[str, Any]