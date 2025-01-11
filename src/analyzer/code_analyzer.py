import os
import re
from git import Repo
from typing import Dict, List, Optional
from dataclasses import dataclass
import radon.complexity as radon_cc
from radon.raw import analyze
from radon.metrics import h_visit

@dataclass
class AnalysisResult:
    code_quality_score: float
    ai_framework_score: float
    execution_score: float
    security_score: float
    issues: List[Dict]
    recommendations: List[str]
    
    def calculate_overall_score(self) -> float:
        """Calculate overall project score using 30/30/30/10 weight distribution"""
        weights = {
            'ai_framework': 0.3,  # 30% - AI Framework Implementation
            'code_quality': 0.3,  # 30% - Code Quality & Patterns
            'execution': 0.3,     # 30% - Execution & Performance
            'security': 0.1       # 10% - Security Measures
        }
        
        return (
            weights['ai_framework'] * self.ai_framework_score +
            weights['code_quality'] * self.code_quality_score +
            weights['execution'] * self.execution_score +
            weights['security'] * self.security_score
        )

class CodeAnalyzer:
    def __init__(self, repo_url: str):
        self.repo_url: str = repo_url
        self.repo_path: Optional[str] = None
        
    async def clone_repository(self) -> str:
        """Clone the repository and return the local path"""
        repo_name = self.repo_url.split('/')[-1]
        self.repo_path = f"/tmp/analysis_{repo_name}"
        
        if os.path.exists(self.repo_path):
            return self.repo_path
            
        Repo.clone_from(self.repo_url, self.repo_path)
        return self.repo_path
        
    async def analyze(self) -> AnalysisResult:
        """Perform complete analysis of the repository"""
        if not self.repo_path:
            await self.clone_repository()
            
        if not self.repo_path:  # Still None after clone attempt
            raise ValueError("Failed to initialize repository path")
            
        # Initialize sub-analyzers
        from .ai_detector import AIFrameworkDetector
        from .execution_verifier import ExecutionVerifier
        
        ai_detector = AIFrameworkDetector(self.repo_path)
        execution_verifier = ExecutionVerifier(self.repo_path)
        
        # Perform analysis
        ai_score = await ai_detector.detect_frameworks()
        exec_score = await execution_verifier.verify_execution()
        
        # Calculate overall scores and collect issues
        return AnalysisResult(
            code_quality_score=self._analyze_code_quality(),
            ai_framework_score=ai_score,
            execution_score=exec_score,
            security_score=self._analyze_security(),
            issues=self._collect_issues(),
            recommendations=self._generate_recommendations()
        )
        
    def _analyze_code_quality(self) -> float:
        """Analyze code quality focusing on AI implementation patterns"""
        total_score = 0.0
        file_count = 0
        
        # AI code quality patterns
        ai_patterns = {
            'model_configuration': r'(model_config|ModelConfig|configuration)\s*=',
            'prompt_templates': r'(PROMPT_TEMPLATE|system_prompt|user_prompt)\s*=',
            'error_handling': r'try\s*{.*?}\s*catch.*?{.*?}',
            'logging': r'(log|logger|console)\.(info|error|debug)',
            'type_annotations': r':\s*(str|int|float|bool|List|Dict|Any)',
            'documentation': r'("""|\'\'\'|\#\s*@)',
            'testing': r'(test_|assert|expect)',
            'modular_structure': r'(class|def|interface|type)\s+\w+',
        }
        
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if not file.endswith(('.py', '.rs', '.ts', '.tsx', '.js', '.jsx')):
                    continue
                    
                file_path = os.path.join(root, file)
                file_count += 1
                
                try:
                    # Base quality score
                    if file.endswith('.py'):
                        base_score = self._analyze_python_quality(file_path)
                    elif file.endswith('.rs'):
                        base_score = self._analyze_rust_quality(file_path)
                    else:
                        base_score = self._analyze_typescript_quality(file_path)
                    
                    # AI-specific quality score
                    with open(file_path, 'r') as f:
                        content = f.read()
                    ai_score = sum(
                        1 for pattern in ai_patterns.values()
                        if re.search(pattern, content)
                    ) / len(ai_patterns)
                    
                    # Combined score with emphasis on AI patterns
                    total_score += (base_score * 0.4 + ai_score * 0.6)
                except Exception as e:
                    print(f"Error analyzing {file}: {e}")
                    continue
        
        return total_score / max(file_count, 1)
        
    def _analyze_python_quality(self, file_path: str) -> float:
        """Analyze Python code quality using radon"""
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Calculate cyclomatic complexity
        blocks = radon_cc.cc_visit(content)
        if blocks:
            complexity_scores = [block.complexity for block in blocks]
            avg_complexity = sum(complexity_scores) / len(complexity_scores)
            complexity_score = max(0, 1 - (avg_complexity / 10))  # Normalize, lower is better
        else:
            complexity_score = 1.0
            
        # Calculate maintainability index
        mi_score = h_visit(content)
        mi_normalized = max(0, min(1, mi_score / 100))  # Convert to 0-1 scale
        
        # Raw metrics
        raw_metrics = analyze(content)
        loc = raw_metrics.loc
        lloc = raw_metrics.lloc
        comments = raw_metrics.comments
        
        # Calculate documentation ratio
        doc_ratio = comments / max(lloc, 1) if lloc > 0 else 0
        doc_score = min(1, doc_ratio * 2)  # Scale up to reward documentation
        
        # Weighted average of all metrics
        return (complexity_score * 0.4 + mi_normalized * 0.4 + doc_score * 0.2)
        
    def _analyze_rust_quality(self, file_path: str) -> float:
        """Analyze Rust code quality using basic metrics"""
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Count lines of code and comments
        lines = content.split('\n')
        total_lines = len(lines)
        comment_lines = len([l for l in lines if l.strip().startswith('//') or l.strip().startswith('/*')])
        doc_lines = len([l for l in lines if l.strip().startswith('///')])
        
        # Calculate documentation ratio
        doc_ratio = (comment_lines + doc_lines) / max(total_lines, 1)
        doc_score = min(1, doc_ratio * 2)
        
        # Check for proper error handling
        error_handling_patterns = [
            r'Result<.*>',
            r'Option<.*>',
            r'match .*',
            r'\.unwrap_or\(',
            r'\.unwrap_or_else\(',
            r'\.map_err\(',
        ]
        error_handling_score = sum(
            1 for pattern in error_handling_patterns
            if re.search(pattern, content)
        ) / len(error_handling_patterns)
        
        # Check for proper type annotations and documentation
        type_patterns = [
            r'pub struct .*',
            r'pub enum .*',
            r'pub trait .*',
            r'pub fn .*',
            r'impl .*',
        ]
        type_score = sum(
            1 for pattern in type_patterns
            if re.search(pattern, content)
        ) / max(len(type_patterns), 1)
        
        # Weighted average of all metrics
        return (doc_score * 0.3 + error_handling_score * 0.4 + type_score * 0.3)
        
    def _analyze_typescript_quality(self, file_path: str) -> float:
        """Analyze TypeScript/JavaScript code quality"""
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Count lines of code and comments
        lines = content.split('\n')
        total_lines = len(lines)
        comment_lines = len([l for l in lines if l.strip().startswith('//') or l.strip().startswith('/*')])
        
        # Calculate documentation ratio
        doc_ratio = comment_lines / max(total_lines, 1)
        doc_score = min(1, doc_ratio * 2)
        
        # Check for proper type annotations (TypeScript)
        type_patterns = [
            r'interface\s+\w+',
            r'type\s+\w+\s*=',
            r':\s*(string|number|boolean|any)\b',
            r'<\w+\s*extends\s*\w+>',
            r'as\s+const',
        ]
        type_score = sum(
            1 for pattern in type_patterns
            if re.search(pattern, content)
        ) / len(type_patterns)
        
        # Check for React/Next.js best practices
        react_patterns = [
            r'export\s+(default\s+)?function\s+\w+',
            r'const\s+\w+\s*=\s*\([^)]*\)\s*:',
            r'useState<',
            r'useEffect',
            r'Props\>',
        ]
        react_score = sum(
            1 for pattern in react_patterns
            if re.search(pattern, content)
        ) / len(react_patterns)
        
        # Check for error handling
        error_patterns = [
            r'try\s*{',
            r'catch\s*\(',
            r'throw\s+new\s+Error',
            r'Promise\.catch',
            r'Error\>',
        ]
        error_score = sum(
            1 for pattern in error_patterns
            if re.search(pattern, content)
        ) / len(error_patterns)
        
        # Weighted average of all metrics
        return (doc_score * 0.2 + type_score * 0.3 + react_score * 0.3 + error_score * 0.2)
        
    def _analyze_security(self) -> float:
        """Analyze security issues"""
        total_score = 0.0
        file_count = 0
        
        security_patterns = {
            'api_key_exposure': r'(API_KEY|OPENAI_KEY|ANTHROPIC_KEY|COHERE_KEY|SECRET_KEY)\s*=\s*["\'][^"\']+["\']',
            'model_input_validation': r'(validate_prompt|sanitize_input|clean_text)\s*\(',
            'token_limit_check': r'(max_tokens|token_limit|check_length)\s*[=<>]',
            'rate_limiting': r'(RateLimit|rateLimiter|throttle|delay)\s*\(',
            'error_handling': r'try\s*{.*?}\s*catch.*?{.*?}',
            'secure_api_calls': r'https?://[^"\']+api[^"\']*',
            'input_sanitization': r'(sanitize|escape|clean|validate).*?(input|text|prompt)',
            'model_output_validation': r'(validate_response|check_output|filter_result)',
        }
        
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if not file.endswith(('.py', '.rs', '.ts', '.tsx', '.js', '.jsx')):
                    continue
                    
                file_path = os.path.join(root, file)
                file_count += 1
                
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Check for security patterns
                    security_issues = sum(1 for pattern in security_patterns.values()
                                       if not re.search(pattern, content))
                    
                    # Calculate security score (inverse of issues)
                    score = 1 - (security_issues / len(security_patterns))
                    total_score += max(0, score)  # Ensure non-negative
                except Exception as e:
                    print(f"Error analyzing security for {file}: {e}")
                    continue
        
        return total_score / max(file_count, 1)
        
    def _collect_issues(self) -> List[Dict]:
        """Collect all identified issues"""
        return []
        
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis"""
        return []
