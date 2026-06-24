"""
Metrics Models
"""
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class PipelineMetrics:
    """Pipeline performance metrics"""
    total_requests: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_retries: int = 0
    total_repairs: int = 0
    total_latency: float = 0.0
    latency_history: List[float] = field(default_factory=list)
    
    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return (self.success_count / self.total_requests) * 100
    
    @property
    def avg_latency_ms(self) -> float:
        if not self.latency_history:
            return 0.0
        return (sum(self.latency_history) / len(self.latency_history)) * 1000
    
    def to_dict(self) -> dict:
        return {
            'total_requests': self.total_requests,
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'total_retries': self.total_retries,
            'total_repairs': self.total_repairs,
            'success_rate': self.success_rate,
            'avg_latency_ms': self.avg_latency_ms
        }