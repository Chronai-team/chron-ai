from setuptools import setup, find_packages

setup(
    name="chron-analyzer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "pydantic>=2.4.2",
        "gitpython>=3.1.40",
        "pytest>=7.4.3",
        "pytest-asyncio>=0.21.1",
        "pylint>=3.0.2",
        "radon>=6.0.1",
        "bandit>=1.7.5",
        "tensorflow-hub>=0.15.0",
        "torch>=2.2.0",
        "transformers>=4.35.2",
        "solana>=0.30.2",
        "anchorpy>=0.18.0",
    ],
    python_requires=">=3.8",
)
