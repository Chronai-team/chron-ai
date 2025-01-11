import pytest
from analyzer.code_analyzer import CodeAnalyzer, AnalysisResult
import tempfile
import os
import shutil

@pytest.fixture
def temp_repo():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def create_test_repo(repo_path: str):
    """Create a test repository with AI-related code"""
    os.makedirs(repo_path, exist_ok=True)
    
    # Create a file with AI imports
    with open(os.path.join(repo_path, "model.py"), "w") as f:
        f.write("""
import tensorflow as tf
import torch
from transformers import AutoModel

def create_model():
    return tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
""")
    
    # Create a file with execution issues
    with open(os.path.join(repo_path, "broken.py"), "w") as f:
        f.write("def broken_function() pass  # Syntax error")

@pytest.mark.asyncio
async def test_full_analysis():
    with tempfile.TemporaryDirectory() as temp_dir:
        create_test_repo(temp_dir)
        analyzer = CodeAnalyzer("dummy_url")
        analyzer.repo_path = temp_dir
        
        result = await analyzer.analyze()
        assert isinstance(result, AnalysisResult)
        assert result.ai_framework_score > 0
        assert result.execution_score < 1  # Due to broken.py
        assert isinstance(result.issues, list)
        assert isinstance(result.recommendations, list)
