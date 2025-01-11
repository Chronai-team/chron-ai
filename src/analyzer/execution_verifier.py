import os
import re
import ast
from typing import List, Dict

class ExecutionVerifier:
    """Verifies if the code can actually execute and perform AI operations"""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        
    async def verify_execution(self) -> float:
        """
        Verify if the code can execute and perform AI operations
        Returns a score between 0 and 1
        """
        # Check for basic executability
        syntax_score = self._check_syntax()
        
        # Check for proper AI function implementation
        implementation_score = await self._check_implementation()
        
        # Check for proper dependency management
        dependency_score = self._check_dependencies()
        
        # Weight implementation more heavily for AI projects
        # Implementation is most important, followed by syntax, then dependencies
        return (syntax_score * 0.25 + implementation_score * 0.65 + dependency_score * 0.1)
        
    def _check_syntax(self) -> float:
        """Check if the code has valid syntax"""
        valid_files = 0
        total_files = 0
        
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if not file.endswith('.py'):
                    continue
                    
                total_files += 1
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        ast.parse(f.read())
                    valid_files += 1
                except SyntaxError:
                    continue
                    
        return valid_files / max(total_files, 1)
        
    async def _check_implementation(self) -> float:
        """Check if AI-related functions are properly implemented"""
        implementation_score = 0.0
        total_checks = 0
        
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if not file.endswith(('.py', '.rs')):
                    continue
                    
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                
                # Check for AI model initialization
                if self._check_model_init(content):
                    implementation_score += 1
                    total_checks += 1
                
                # Check for inference/prediction methods
                if self._check_inference_methods(content):
                    implementation_score += 1
                    total_checks += 1
                
                # Check for proper error handling in AI operations
                if self._check_ai_error_handling(content):
                    implementation_score += 1
                    total_checks += 1
                    
                # Check for model configuration
                if self._check_model_config(content):
                    implementation_score += 1
                    total_checks += 1
        
        return implementation_score / max(total_checks, 1)
        
    def _check_model_init(self, content: str) -> bool:
        """Check for proper model initialization"""
        patterns = [
            r'CompletionModel::new',
            r'EmbeddingModel::new',
            r'Agent::new',
            r'model\s*=\s*[A-Za-z]+Model\(',
            r'torch\.nn\.Module',
            r'keras\.Model',
        ]
        return any(re.search(pattern, content) for pattern in patterns)
        
    def _check_inference_methods(self, content: str) -> bool:
        """Check for inference/prediction methods"""
        patterns = [
            r'async\s+fn\s+completion',
            r'async\s+fn\s+embed',
            r'fn\s+forward',
            r'def\s+predict',
            r'def\s+forward',
            r'model\.predict',
        ]
        return any(re.search(pattern, content) for pattern in patterns)
        
    def _check_ai_error_handling(self, content: str) -> bool:
        """Check for AI-specific error handling"""
        patterns = [
            r'CompletionError',
            r'EmbeddingError',
            r'Result<.*Response',
            r'try:.*except\s+(torch|tensorflow|transformers)',
        ]
        return any(re.search(pattern, content) for pattern in patterns)
        
    def _check_model_config(self, content: str) -> bool:
        """Check for model configuration"""
        patterns = [
            r'temperature\s*=',
            r'max_tokens\s*=',
            r'model_name\s*=',
            r'batch_size\s*=',
            r'learning_rate\s*=',
        ]
        return any(re.search(pattern, content) for pattern in patterns)
        
    def _check_dependencies(self) -> float:
        """Check if all required dependencies are properly specified"""
        # TODO: Implement dependency verification
        return 0.5
