import json
import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# THE CRITICAL LINE: Must be at the top level for Uvicorn to find it
app = FastAPI(title="ResearchPilot AI Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. INITIALIZE THE CORE
try:
    from agents.core.orchestrator import ResearchOrchestrator
    orchestrator = ResearchOrchestrator()
    print("✅ Cognitive Core (Agents & FAISS) Loaded Successfully")
except Exception as e:
    print(f"❌ Error Loading Orchestrator: {e}")
    orchestrator = None

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)