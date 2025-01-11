# API Documentation

## Overview

Chron AI provides a RESTful API interface for analyzing AI projects on the Solana blockchain.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Analyze Project

Analyze AI project code in a specified GitHub repository.

**Request**

```http
POST /analyze
Content-Type: application/json
```

**Request Parameters**

```json
{
    "repo_url": "string",     // GitHub repository URL
    "additional_info": {      // Optional additional information
        "branch": "string",   // Specify branch (optional)
        "commit": "string"    // Specify commit (optional)
    }
}
```

**Response**

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
        },
        "issues": [
            {
                "type": "warning",
                "message": "Missing error handling",
                "file": "src/model.py",
                "line": 42
            }
        ],
        "recommendations": [
            "Add unit tests",
            "Improve error handling mechanism"
        ]
    }
}
```

**Status Codes**

- 200: Success
- 400: Invalid Request Parameters
- 404: Repository Not Found
- 500: Internal Server Error

### Usage Examples

Using curl to send requests:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/username/project",
    "additional_info": {
        "branch": "main"
    }
  }'
```

Using Python to send requests:

```python
import requests

url = "http://localhost:8000/analyze"
data = {
    "repo_url": "https://github.com/username/project",
    "additional_info": {
        "branch": "main"
    }
}

response = requests.post(url, json=data)
result = response.json()

print(f"Analysis Result: {result}")
```

### Error Handling

When an error occurs, the API will return a response in the following format:

```json
{
    "success": false,
    "error": {
        "code": "ERROR_CODE",
        "message": "Error description"
    }
}
```

Common Error Codes:

- `INVALID_REPO`: Invalid repository URL
- `CLONE_FAILED`: Repository clone failed
- `ANALYSIS_FAILED`: Analysis process failed
- `INVALID_PARAMS`: Invalid request parameters

## Notes

1. API requests require the target repository to be accessible
2. Analysis of large projects may take longer
3. Set reasonable timeout values in requests
4. Frequent requests may be rate-limited

## Best Practices

1. Implement request retry mechanism
2. Cache analysis results
3. Handle long-running analysis tasks asynchronously
4. Monitor analysis progress
