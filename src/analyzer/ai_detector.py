import os
from typing import Dict, List, Set

class AIFrameworkDetector:
    """Detects AI/ML frameworks and validates their implementation"""
    
    KNOWN_AI_FRAMEWORKS = {
        'tensorflow': {
            'imports': {'import tensorflow', 'import tf'},
            'patterns': {'model = tf', 'keras.Sequential', 'keras.layers'}
        },
        'pytorch': {
            'imports': {'import torch', 'from torch'},
            'patterns': {'torch.nn', 'torch.optim', 'model.forward'}
        },
        'transformers': {
            'imports': {'from transformers', 'import transformers'},
            'patterns': {'AutoModel', 'AutoTokenizer', 'pipeline'}
        },
        'openai': {
            'imports': {'import openai', 'from openai', 'OpenAI', 'import { Configuration, OpenAIApi }'},
            'patterns': {
                'openai.Completion', 'openai.ChatCompletion', 
                'new OpenAI(', 'OpenAIApi', 'gpt-4', 'gpt-3.5-turbo',
                'createChatCompletion', 'createCompletion'
            }
        },
        'langchain': {
            'imports': {'from langchain', 'import langchain', 'import { LangChain }'},
            'patterns': {'LLMChain', 'PromptTemplate', 'ChatPromptTemplate'}
        },
        'rig': {
            'imports': {'use rig', 'from rig'},
            'patterns': {'CompletionModel', 'EmbeddingModel', 'Agent'}
        },
        'react-ai': {
            'imports': {'import { useCompletion }', 'import { useChat }', 'import { useModel }'},
            'patterns': {
                'useCompletion', 'useChat', 'useModel',
                'generateText', 'generateCompletion',
                'model: registry.languageModel'
            }
        },
        'next-ai': {
            'imports': {'import { OpenAIStream }', 'import { LangChainStream }'},
            'patterns': {
                'OpenAIStream', 'LangChainStream',
                'experimental_StreamData',
                'createParser', 'EventSource'
            }
        }
    }
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        
    async def detect_frameworks(self) -> float:
        """
        Detect AI frameworks and validate their implementation
        Returns a score between 0 and 1
        """
        self.framework_scores = {}
        detected = self._find_framework_implementations()
        if not detected:
            return 0.0
            
        # Calculate weighted score based on implementation quality
        total_score = sum(self.framework_scores.values())
        max_possible = len(self.framework_scores) * 1.0
        
        return min(1.0, total_score / max_possible if max_possible > 0 else 0.0)
        
    def _find_framework_implementations(self) -> Set[str]:
        """Find AI framework implementations in the codebase"""
        detected_frameworks = set()
        framework_scores = {}
        
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if not file.endswith(('.py', '.rs', '.ts', '.tsx', '.js', '.jsx')):  # Support Python, Rust, and TypeScript/JavaScript
                    continue
                    
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    
                for framework, patterns in self.KNOWN_AI_FRAMEWORKS.items():
                    score = 0
                    # Check imports
                    if any(pattern in content for pattern in patterns['imports']):
                        score += 0.5
                    # Check actual implementation patterns
                    if any(pattern in content for pattern in patterns['patterns']):
                        score += 0.5
                        
                    if score > 0:
                        framework_scores[framework] = max(
                            score,
                            framework_scores.get(framework, 0)
                        )
                        if score > 0.7:  # Strong evidence of implementation
                            detected_frameworks.add(framework)
        
        # Update instance variable for use in scoring
        self.framework_scores = framework_scores
        return detected_frameworks
        
    def _analyze_implementation(self, frameworks: Set[str]) -> float:
        """
        Analyze how well the AI frameworks are implemented
        Returns a score between 0 and 1
        """
        # TODO: Implement deeper analysis of framework usage
        return len(frameworks) / len(self.KNOWN_AI_FRAMEWORKS)
