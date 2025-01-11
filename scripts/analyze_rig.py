#!/usr/bin/env python3
import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path

# Add the src directory to Python path
src_dir = str(Path(__file__).parent.parent / "src")
sys.path.append(src_dir)

from analyzer import CodeAnalyzer

async def main():
    """Analyze AI projects using Chron AI analyzer"""
    try:
        if len(sys.argv) < 2:
            print("Usage: python analyze_project.py <github_url>")
            return 1
            
        repo_url = sys.argv[1]
        print(f"\nStarting AI Project Analysis for: {repo_url}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        analyzer = CodeAnalyzer(repo_url)
        result = await analyzer.analyze()
        
        # Calculate weighted overall score (30/30/30/10 distribution)
        weights = {
            'ai_framework': 0.3,  # 30% - AI/ML Implementation
            'code_quality': 0.3,  # 30% - Code Structure & Patterns
            'execution': 0.3,     # 30% - Runtime & Performance
            'security': 0.1       # 10% - Security Measures
        }
        
        # Calculate weighted score on 10-point scale
        overall_score = 10.0 * (
            weights['ai_framework'] * result.ai_framework_score +
            weights['code_quality'] * result.code_quality_score +
            weights['execution'] * result.execution_score +
            weights['security'] * result.security_score
        )
        
        # Print detailed analysis results
        print("## Chron AI Analysis Results\n")
        print("### Component Scores (0-10 scale)")
        print("1. AI Framework Implementation")
        print(f"   Score: {10.0 * result.ai_framework_score:.1f}/10")
        print("   Evaluates: AI model integration, prompt engineering, context handling")
        print("\n2. Code Quality & Patterns")
        print(f"   Score: {10.0 * result.code_quality_score:.1f}/10")
        print("   Evaluates: AI-specific patterns, documentation, error handling")
        print("\n3. Execution & Performance")
        print(f"   Score: {10.0 * result.execution_score:.1f}/10")
        print("   Evaluates: Runtime efficiency, resource management, reliability")
        print("\n4. Security Measures")
        print(f"   Score: {10.0 * result.security_score:.1f}/10")
        print("   Evaluates: Input validation, API security, model output handling")
        print("\n### Overall Project Score")
        print(f"Final Score: {overall_score:.1f}/10")
        print("Weight Distribution: 30/30/30/10 (AI/Code/Execution/Security)\n")
        
        if result.issues:
            print("### Areas for Improvement")
            for issue in result.issues:
                print(f"- {issue}")
            print()
            
        if result.recommendations:
            print("### Enhancement Recommendations")
            for rec in result.recommendations:
                print(f"- {rec}")
            print()
            
        # Score interpretation guide
        print("### Score Interpretation Guide")
        print("9.0-10.0: Exceptional - Production-ready AI implementation")
        print("7.5-8.9:  Strong     - Well-implemented with minor improvements needed")
        print("6.0-7.4:  Good       - Solid foundation with room for enhancement")
        print("4.0-5.9:  Fair       - Basic implementation, needs significant work")
        print("0.0-3.9:  Limited    - Major improvements required\n")
            
        print("Analysis completed successfully.")
        return 0
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
