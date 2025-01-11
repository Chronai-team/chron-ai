#!/usr/bin/env python3
import sys
from pathlib import Path

# Add the src directory to Python path
src_dir = str(Path(__file__).parent.parent / "src")
sys.path.append(src_dir)

def verify_environment():
    """Verify that all required components are available"""
    try:
        from analyzer import (
            CodeAnalyzer,
            AIFrameworkDetector,
            ExecutionVerifier,
            ReportGenerator
        )
        print("Successfully imported all analyzer components")
        return 0
    except ImportError as e:
        print(f"Environment verification failed: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(verify_environment())
