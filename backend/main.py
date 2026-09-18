from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analyzer import analyze_pipeline_failure
import datetime

app = FastAPI(
    title="DevFlow AI",
    description="AI-powered CI/CD failure analyzer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store analyses in memory
analyses = []

class PipelineLog(BaseModel):
    log: str
    pipeline_name: str = "Unknown Pipeline"

@app.get("/")
def home():
    return {
        "product": "DevFlow AI",
        "tagline": "Paste your failed pipeline log. Get the fix in seconds.",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": str(datetime.datetime.now())}

@app.post("/analyze")
async def analyze(payload: PipelineLog):
    try:
        result = analyze_pipeline_failure(payload.log)
        
        analysis = {
            "id": len(analyses) + 1,
            "pipeline_name": payload.pipeline_name,
            "timestamp": str(datetime.datetime.now()),
            "result": result
        }
        analyses.append(analysis)
        
        return {
            "success": True,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analyses")
def get_analyses():
    return {
        "total": len(analyses),
        "analyses": analyses
    }

@app.get("/stats")
def stats():
    severities = {}
    for a in analyses:
        s = a["result"].get("severity", "Unknown")
        severities[s] = severities.get(s, 0) + 1
    
    return {
        "total_analyses": len(analyses),
        "severity_breakdown": severities,
        "time_saved_minutes": len(analyses) * 45
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
