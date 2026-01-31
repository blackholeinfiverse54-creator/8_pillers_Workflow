"""
Insight Flow Bridge - Agent Routing Integration
Port: 8006
Purpose: Integrate Insight Flow's intelligent routing with BHIV Core
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Insight Flow Bridge", version="1.0.0")

# Configuration
INSIGHT_FLOW_URL = "http://localhost:8007"  # Insight Flow backend
CORE_URL = "http://localhost:8002"
BUCKET_URL = "http://localhost:8001"
KARMA_URL = "http://localhost:8000"

class RoutingRequest(BaseModel):
    input_data: Dict[str, Any]
    input_type: str
    strategy: str = "q_learning"
    context: Optional[Dict] = None

class AgentRouteRequest(BaseModel):
    agent_type: str
    context: Optional[Dict] = None
    confidence_threshold: float = 0.75

@app.get("/health")
def health():
    """Health check"""
    return {
        "status": "ok",
        "service": "Insight Flow Bridge",
        "version": "1.0.0",
        "insight_flow_url": INSIGHT_FLOW_URL
    }

@app.post("/route")
async def route_request(request: RoutingRequest):
    """
    Route request through Insight Flow's intelligent routing
    Then forward to appropriate BHIV Core agent
    """
    try:
        # Call Insight Flow routing
        response = requests.post(
            f"{INSIGHT_FLOW_URL}/api/v2/routing/route",
            json=request.dict(),
            timeout=5
        )
        
        if response.status_code == 200:
            routing_result = response.json()
            
            # Extract selected agent
            selected_agent = routing_result.get("selected_agent", {})
            agent_name = selected_agent.get("name", "edumentor_agent")
            confidence = routing_result.get("confidence_score", 0.0)
            
            # Forward to Core if confidence is high enough
            if confidence >= 0.7:
                core_response = requests.post(
                    f"{CORE_URL}/handle_task",
                    json={
                        "agent": agent_name,
                        "input": request.input_data.get("text", ""),
                        "input_type": request.input_type
                    },
                    timeout=10
                )
                
                return {
                    "routing": routing_result,
                    "core_response": core_response.json() if core_response.status_code == 200 else None,
                    "status": "success"
                }
            else:
                return {
                    "routing": routing_result,
                    "status": "low_confidence",
                    "message": f"Confidence {confidence} below threshold"
                }
        else:
            raise HTTPException(status_code=response.status_code, detail="Insight Flow routing failed")
            
    except Exception as e:
        logger.error(f"Routing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/route-agent")
async def route_agent(request: AgentRouteRequest):
    """Route to best agent based on type and context"""
    try:
        response = requests.post(
            f"{INSIGHT_FLOW_URL}/api/v1/routing/route-agent",
            json=request.dict(),
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Agent routing failed")
            
    except Exception as e:
        logger.error(f"Agent routing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_analytics():
    """Get routing analytics from Insight Flow"""
    try:
        response = requests.get(
            f"{INSIGHT_FLOW_URL}/api/v1/analytics/overview",
            params={"time_range": "24h"},
            timeout=5
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Analytics unavailable"}
            
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        return {"error": str(e)}

@app.get("/metrics")
def get_metrics():
    """Get bridge metrics"""
    return {
        "bridge_version": "1.0.0",
        "insight_flow_url": INSIGHT_FLOW_URL,
        "core_url": CORE_URL,
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
