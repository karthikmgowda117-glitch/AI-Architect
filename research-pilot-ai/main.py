import json
import uvicorn
import sys
import os
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# Ensure the 'agents' folder is findable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 1. DEFINE THE APP (MUST BE AT THE TOP LEVEL - NO INDENTATION)
app = FastAPI(title="ResearchPilot AI Core")

# 2. SETUP CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. INITIALIZE THE CORE
try:
    from agents.core.orchestrator import ResearchOrchestrator
    orchestrator = ResearchOrchestrator()
    print("✅ Cognitive Core Loaded Successfully")
except Exception as e:
    print(f"❌ Error Loading Orchestrator: {e}")
    orchestrator = None

# --- ROUTES ---

@app.get("/")
async def root():
    return {"status": "online", "message": "ResearchPilot AI Core is running."}

@app.get("/research")
async def stream_research(topic: str = Query(...)):
    async def event_generator():
        if not orchestrator:
            yield f"data: {json.dumps({'type': 'error', 'msg': 'Orchestrator not initialized'})}\n\n"
            return
            
        try:
            async for update in orchestrator.run_mission(topic):
                yield f"data: {json.dumps(update)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'msg': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# --- SERVER START ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)