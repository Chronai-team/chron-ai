import pytest
from analyzer import CodeAnalyzer

@pytest.mark.asyncio
async def test_rig_project():
    """Test analysis of the rig project which has real AI functionality"""
    analyzer = CodeAnalyzer('https://github.com/0xPlaygrounds/rig')
    result = await analyzer.analyze()
    
    # Verify AI framework detection
    assert result.ai_framework_score > 0.7, "Should detect strong AI framework presence"
    
    # Verify code quality
    assert result.code_quality_score > 0, "Should have valid code quality score"
    
    # Verify execution capability
    assert result.execution_score > 0.7, "Should have high execution score"
    
    # Print detailed results for manual verification
    print('\nAnalysis Results for rig:')
    print(f'AI Framework Score: {result.ai_framework_score}')
    print(f'Code Quality Score: {result.code_quality_score}')
    print(f'Execution Score: {result.execution_score}')
    print(f'Security Score: {result.security_score}')
    
    if result.issues:
        print('\nIssues:', result.issues)
    if result.recommendations:
        print('\nRecommendations:', result.recommendations)

@pytest.mark.asyncio
async def test_mage_project():
    """Test analysis of the mage project to verify AI functionality"""
    analyzer = CodeAnalyzer('https://github.com/mage-terminal/mage')
    result = await analyzer.analyze()
    
    # Verify AI framework detection - expecting high score due to GPT-4, transformers, and LSTM
    assert result.ai_framework_score > 0.7, "Should detect strong AI framework presence (GPT-4, transformers, LSTM)"
    
    # Verify code quality - expecting moderate to high score due to well-structured code
    assert result.code_quality_score > 0.5, "Should have good code quality score"
    
    # Verify execution capability - expecting high score due to proper implementation
    assert result.execution_score > 0.7, "Should have high execution score"
    
    # Verify security measures - expecting basic security implementation
    assert result.security_score > 0.3, "Should have basic security measures"
    
    # Print detailed results for manual verification
    print('\nAnalysis Results for mage:')
    print(f'AI Framework Score: {result.ai_framework_score}')
    print(f'Code Quality Score: {result.code_quality_score}')
    print(f'Execution Score: {result.execution_score}')
    print(f'Security Score: {result.security_score}')
    
    if result.issues:
        print('\nIssues:', result.issues)
    if result.recommendations:
        print('\nRecommendations:', result.recommendations)
