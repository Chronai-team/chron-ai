import pytest
from analyzer.execution_verifier import ExecutionVerifier
import os
import tempfile
import shutil

@pytest.fixture
def temp_repo():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def execution_verifier(temp_repo):
    return ExecutionVerifier(temp_repo)

def create_test_file(repo_path: str, content: str, filename: str = "test.py"):
    """Helper to create test files"""
    file_path = os.path.join(repo_path, filename)
    with open(file_path, "w") as f:
        f.write(content)

async def test_valid_syntax(temp_repo, execution_verifier):
    create_test_file(temp_repo, """
def test_function():
    return "Hello, World!"
""")
    score = await execution_verifier.verify_execution()
    assert score > 0

async def test_invalid_syntax(temp_repo, execution_verifier):
    create_test_file(temp_repo, """
def test_function()
    return "Missing colon"
""")
    score = await execution_verifier.verify_execution()
    assert score < 1

async def test_multiple_files(temp_repo, execution_verifier):
    create_test_file(temp_repo, "def func1(): pass", "file1.py")
    create_test_file(temp_repo, "def func2(): pass", "file2.py")
    create_test_file(temp_repo, "invalid python code", "file3.py")
    score = await execution_verifier.verify_execution()
    assert 0 < score < 1  # Some files valid, some invalid
