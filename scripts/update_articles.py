#!/usr/bin/env python3
import re
import glob
import os
from pathlib import Path

def extract_scores(report_path):
    """Extract scores from analysis report"""
    with open(report_path, "r") as f:
        content = f.read()
    
    # Extract scores using regex
    ai_score = re.search(r"AI Framework.*?(\d+\.\d+)/10", content, re.DOTALL)
    code_score = re.search(r"Code Quality.*?(\d+\.\d+)/10", content, re.DOTALL)
    exec_score = re.search(r"Execution.*?(\d+\.\d+)/10", content, re.DOTALL)
    security_score = re.search(r"Security.*?(\d+\.\d+)/10", content, re.DOTALL)
    overall_score = re.search(r"Final Score:\s*(\d+\.\d+)/10", content)
    
    # Print debug info
    print(f"Extracting scores from {report_path}:")
    print(f"AI Framework Score: {ai_score.group(1) if ai_score else 'Not found'}")
    print(f"Code Quality Score: {code_score.group(1) if code_score else 'Not found'}")
    print(f"Execution Score: {exec_score.group(1) if exec_score else 'Not found'}")
    print(f"Security Score: {security_score.group(1) if security_score else 'Not found'}")
    print(f"Overall Score: {overall_score.group(1) if overall_score else 'Not found'}\n")
    
    return {
        "ai_score": ai_score.group(1) if ai_score else "0.0",
        "code_score": code_score.group(1) if code_score else "0.0",
        "exec_score": exec_score.group(1) if exec_score else "0.0",
        "security_score": security_score.group(1) if security_score else "0.0",
        "overall_score": overall_score.group(1) if overall_score else "0.0"
    }

def update_article(article_path, scores):
    """Update article with actual scores"""
    with open(article_path, "r") as f:
        content = f.read()
    
    # Replace placeholders with actual scores
    content = content.replace("{ai_score}", scores["ai_score"])
    content = content.replace("{code_score}", scores["code_score"])
    content = content.replace("{exec_score}", scores["exec_score"])
    content = content.replace("{security_score}", scores["security_score"])
    content = content.replace("{overall_score}", scores["overall_score"])
    
    with open(article_path, "w") as f:
        f.write(content)

def main():
    """Update all Medium articles with scores from analysis reports"""
    # Get the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Process each project
    for report_path in glob.glob(str(project_root / "reports/analysis/*_analysis_report.md")):
        match = re.search(r"(\w+)_analysis_report", report_path)
        if not match:
            print(f"Could not extract project name from {report_path}")
            continue
            
        project = match.group(1)
        scores = extract_scores(report_path)
        article_path = project_root / f"reports/medium/{project}_article.md"
        
        if os.path.exists(article_path):
            update_article(str(article_path), scores)
            print(f"Updated article for {project} with scores: {scores}")
        else:
            print(f"Article not found: {article_path}")

if __name__ == "__main__":
    main()
