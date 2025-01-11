from typing import Dict, List
from dataclasses import dataclass
from .code_analyzer import AnalysisResult

@dataclass
class Report:
    overall_score: float
    detailed_scores: Dict[str, float]
    issues: List[Dict]
    recommendations: List[str]

class ReportGenerator:
    """Generates analysis reports in various formats"""
    
    def __init__(self, analysis_result: AnalysisResult):
        self.result = analysis_result
        
    def generate_summary(self) -> Report:
        """Generate a summary report"""
        overall_score = self._calculate_overall_score()
        
        return Report(
            overall_score=overall_score,
            detailed_scores={
                'Code Quality': self.result.code_quality_score,
                'AI Framework Integration': self.result.ai_framework_score,
                'Execution Verification': self.result.execution_score,
                'Security': self.result.security_score
            },
            issues=self.result.issues,
            recommendations=self.result.recommendations
        )
        
    def _calculate_overall_score(self) -> float:
        """Calculate the overall project score"""
        weights = {
            'code_quality': 0.2,
            'ai_framework': 0.3,
            'execution': 0.4,
            'security': 0.1
        }
        
        return (
            weights['code_quality'] * self.result.code_quality_score +
            weights['ai_framework'] * self.result.ai_framework_score +
            weights['execution'] * self.result.execution_score +
            weights['security'] * self.result.security_score
        )
