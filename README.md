![image](https://github.com/user-attachments/assets/a4a82767-bb79-44d3-87f3-3bc4f26fc281)
# Chron AI Analysis Tool

Chron AI is a specialized tool for analyzing and verifying the authenticity of AI projects on the Solana blockchain. It can detect whether projects have genuine AI functionality implementation, rather than just placeholder code.

## Features

- 🔍 AI Framework Detection: Identify AI frameworks and libraries used in projects
- ⚡ Execution Verification: Validate if AI-related code can actually run
- 📊 Code Quality Analysis: Evaluate code quality and maintainability
- 🛡️ Security Check: Detect potential security issues

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Chronai-team/chronai.git
cd chronai
```

2. Install dependencies:
```bash
pip install -e .
```

## Usage

### Command Line

```bash
# Start the analysis server
python src/main.py
```

### API Usage

Send a project analysis request to the API:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/username/project"}'
```

### Analysis Results

The analysis report includes the following key metrics:

1. AI Framework Score
   - 0.7+ : Complete AI framework implementation
   - 0.4-0.7: Partial AI functionality
   - <0.4: Lacks substantial AI features

2. Execution Score
   - 0.7+: Code executes normally
   - 0.4-0.7: Has partial execution issues
   - <0.4: Serious execution problems

3. Code Quality Score
   - 0.7+: High quality code
   - 0.4-0.7: Medium quality
   - <0.4: Needs improvement

4. Security Score
   - 0.7+: Good security
   - 0.4-0.7: Potential risks exist
   - <0.4: Serious security concerns

## Example

Analysis results for the [rig](https://github.com/0xPlaygrounds/rig) project:

```json
{
    "success": true,
    "report": {
        "overall_score": 0.71,
        "detailed_scores": {
            "AI Framework Integration": 0.75,
            "Code Quality": 0.34,
            "Execution Verification": 0.75,
            "Security": 0.0
        }
    }
}
```

This result indicates:
- ✅ Project has genuine AI functionality (AI Framework Score: 0.75)
- ✅ Code executes normally (Execution Score: 0.75)
- ⚠️ Code quality needs improvement (Code Quality Score: 0.34)
- ⚠️ Security measures need strengthening (Security Score: 0.0)

## Notes

1. Ensure sufficient system permissions to clone and analyze target repositories
2. Analysis of large projects may take longer
3. Some private repositories may require additional authentication

## Contributing

Pull Requests to improve this tool are welcome. Please ensure:

1. Add appropriate test cases
2. Update relevant documentation
3. Follow the project's code style

## License

MIT License
