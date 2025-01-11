from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from analyzer import CodeAnalyzer, ReportGenerator

app = FastAPI(
    title="Solana AI Project Analyzer",
    description="Analyzes Solana projects claiming AI capabilities",
    version="1.0.0"
)

class AnalysisRequest(BaseModel):
    repo_url: str
    additional_info: dict = {}

@app.post("/analyze")
async def analyze_repository(request: AnalysisRequest):
    """Analyze a GitHub repository"""
    try:
        analyzer = CodeAnalyzer(request.repo_url)
        result = await analyzer.analyze()
        
        report_generator = ReportGenerator(result)
        report = report_generator.generate_summary()
        
        return {
            "success": True,
            "report": report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
