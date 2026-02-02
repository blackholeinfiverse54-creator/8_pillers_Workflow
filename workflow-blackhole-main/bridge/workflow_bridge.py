"""
Workflow Blackhole Bridge Service
Connects Workflow Blackhole to 8-Pillar Infrastructure

Port: 8008
Version: 1.0.0
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiohttp
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Workflow Blackhole Bridge",
    description="9th Pillar - Model Layer Integration",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pillar endpoints
PILLARS = {
    "bucket": "http://localhost:8001",
    "karma": "http://localhost:8000",
    "core": "http://localhost:8002",
    "insight": "http://localhost:8005",
    "insight_flow": "http://localhost:8006",
    "uao": "http://localhost:8004",
    "workflow": "http://localhost:8003"
}

PILLAR_TIMEOUT = 2.0

# Pydantic models
class AttendanceEvent(BaseModel):
    user_id: str
    user_name: str
    event_type: str
    timestamp: datetime
    location: Optional[Dict[str, Any]] = None
    hours_worked: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class TaskEvent(BaseModel):
    task_id: str
    title: str
    assignee_id: str
    assignee_name: str
    priority: str
    status: str
    department: str
    metadata: Optional[Dict[str, Any]] = None

class EmployeeActivityEvent(BaseModel):
    user_id: str
    activity_type: str
    timestamp: datetime
    productivity_score: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class SalaryEvent(BaseModel):
    user_id: str
    user_name: str
    month: str
    base_salary: float
    hours_worked: float
    overtime_hours: float
    total_salary: float
    metadata: Optional[Dict[str, Any]] = None

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    pillar_status = {}
    
    # Define health endpoints for each service
    health_endpoints = {
        "bucket": f"{PILLARS['bucket']}/health",
        "karma": f"{PILLARS['karma']}/health",
        "core": f"{PILLARS['core']}/health",
        "insight": f"{PILLARS['insight']}/health",
        "insight_flow": f"{PILLARS['insight_flow']}/health",
        "uao": f"{PILLARS['uao']}/docs",  # UAO uses /docs
        "workflow": f"{PILLARS['workflow']}/healthz"  # Workflow uses /healthz
    }
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        for name, url in health_endpoints.items():
            try:
                async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=3.0)
                ) as resp:
                    pillar_status[name] = "healthy" if resp.status == 200 else "unhealthy"
            except Exception as e:
                pillar_status[name] = f"unreachable: {str(e)[:50]}"
    
    return {
        "status": "healthy",
        "service": "workflow_blackhole_bridge",
        "version": "1.0.0",
        "port": 8008,
        "pillars": pillar_status
    }

@app.post("/bridge/attendance/event")
async def log_attendance_event(event: AttendanceEvent):
    """Log attendance event to Bucket → Karma pipeline"""
    try:
        logger.info(f"📊 Attendance event: {event.event_type} for {event.user_name}")
        
        # 1. Write to Bucket (audit trail)
        bucket_payload = {
            "event_type": "attendance",
            "source": "workflow_blackhole",
            "user_id": event.user_id,
            "user_name": event.user_name,
            "action": event.event_type,
            "timestamp": event.timestamp.isoformat(),
            "data": {
                "location": event.location,
                "hours_worked": event.hours_worked,
                "metadata": event.metadata
            }
        }
        
        bucket_success = False
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{PILLARS['bucket']}/core/write-event",
                    json=bucket_payload,
                    timeout=aiohttp.ClientTimeout(total=PILLAR_TIMEOUT)
                ) as resp:
                    bucket_success = resp.status == 200
                    if bucket_success:
                        logger.info(f"✅ Bucket: Attendance event logged")
            except Exception as e:
                logger.warning(f"⚠️ Bucket write failed: {e}")
        
        # 2. Log to Karma (behavioral tracking)
        karma_payload = {
            "type": "life_event",
            "data": {
                "user_id": event.user_id,
                "action": f"attendance_{event.event_type}",
                "role": "employee",
                "note": f"Attendance: {event.event_type}",
                "hours_worked": event.hours_worked or 0
            },
            "source": "workflow_blackhole"
        }
        
        karma_success = False
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{PILLARS['karma']}/v1/event/",
                    json=karma_payload,
                    timeout=aiohttp.ClientTimeout(total=PILLAR_TIMEOUT)
                ) as resp:
                    karma_success = resp.status == 200
                    if karma_success:
                        logger.info(f"✅ Karma: Behavioral event logged")
            except Exception as e:
                logger.warning(f"⚠️ Karma write failed: {e}")
        
        return {
            "success": True,
            "message": "Attendance event processed",
            "pillars": {
                "bucket": bucket_success,
                "karma": karma_success
            },
            "event_id": f"att_{event.user_id}_{int(event.timestamp.timestamp())}"
        }
    
    except Exception as e:
        logger.error(f"❌ Attendance event error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bridge/task/assign")
async def assign_task_with_ai(task: TaskEvent):
    """Assign task using Core AI + Insight Flow routing"""
    try:
        logger.info(f"🎯 Task assignment: {task.title} → {task.assignee_name}")
        
        # 1. Route through Insight Flow for best agent
        routing_payload = {
            "input": task.title,
            "input_type": "text",
            "metadata": {
                "priority": task.priority,
                "department": task.department
            }
        }
        
        selected_agent = "edumentor_agent"
        routing_success = False
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{PILLARS['insight_flow']}/route-agent",
                    json=routing_payload,
                    timeout=aiohttp.ClientTimeout(total=PILLAR_TIMEOUT)
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        selected_agent = result.get("agent", "edumentor_agent")
                        routing_success = True
                        logger.info(f"✅ Insight Flow: Routed to {selected_agent}")
            except Exception as e:
                logger.warning(f"⚠️ Insight Flow routing failed: {e}")
        
        # 2. Process task through Core (optional AI analysis)
        core_payload = {
            "agent": selected_agent,
            "input": f"Task: {task.title}\nPriority: {task.priority}\nAssignee: {task.assignee_name}",
            "input_type": "text"
        }
        
        ai_response = None
        core_success = False
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{PILLARS['core']}/handle_task",
                    json=core_payload,
                    timeout=aiohttp.ClientTimeout(total=5.0)
                ) as resp:
                    if resp.status == 200:
                        ai_response = await resp.json()
                        core_success = True
                        logger.info(f"✅ Core: Task processed with AI")
            except Exception as e:
                logger.warning(f"⚠️ Core processing failed: {e}")
        
        # 3. Log to Bucket
        bucket_payload = {
            "event_type": "task_assignment",
            "source": "workflow_blackhole",
            "task_id": task.task_id,
            "assignee_id": task.assignee_id,
            "timestamp": datetime.now().isoformat(),
            "data": {
                "title": task.title,
                "priority": task.priority,
                "status": task.status,
                "department": task.department,
                "selected_agent": selected_agent,
                "ai_response": ai_response
            }
        }
        
        bucket_success = False
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{PILLARS['bucket']}/core/write-event",
                    json=bucket_payload,
                    timeout=aiohttp.ClientTimeout(total=PILLAR_TIMEOUT)
                ) as resp:
                    bucket_success = resp.status == 200
            except Exception as e:
                logger.warning(f"⚠️ Bucket write failed: {e}")
        
        return {
            "success": True,
            "message": "Task assigned with AI routing",
            "selected_agent": selected_agent,
            "ai_response": ai_response,
            "pillars": {
                "insight_flow": routing_success,
                "core": core_success,
                "bucket": bucket_success
            }
        }
    
    except Exception as e:
        logger.error(f"❌ Task assignment error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bridge/activity/log")
async def log_employee_activity(activity: EmployeeActivityEvent):
    """Log employee activity to PRANA → Bucket → Karma pipeline"""
    try:
        logger.info(f"📈 Activity: {activity.activity_type} for user {activity.user_id}")
        
        # 1. Create PRANA packet
        prana_packet = {
            "user_id": activity.user_id,
            "session_id": f"wf_{activity.user_id}_{int(activity.timestamp.timestamp())}",
            "system_type": "workflow_blackhole",
            "role": "employee",
            "timestamp": activity.timestamp.isoformat(),
            "cognitive_state": "ON_TASK" if activity.productivity_score and activity.productivity_score > 70 else "IDLE",
            "active_seconds": 5.0,
            "idle_seconds": 0.0,
            "away_seconds": 0.0,
            "focus_score": activity.productivity_score or 50,
            "raw_signals": {
                "activity_type": activity.activity_type,
                "metadata": activity.metadata
            }
        }
        
        # 2. Send to Bucket PRANA ingestion
        prana_success = False
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{PILLARS['bucket']}/bucket/prana/ingest",
                    json=prana_packet,
                    timeout=aiohttp.ClientTimeout(total=PILLAR_TIMEOUT)
                ) as resp:
                    prana_success = resp.status == 200
                    if prana_success:
                        logger.info(f"✅ PRANA: Activity logged")
            except Exception as e:
                logger.warning(f"⚠️ PRANA ingestion failed: {e}")
        
        return {
            "success": True,
            "message": "Activity logged to PRANA pipeline",
            "pillars": {
                "prana": prana_success
            }
        }
    
    except Exception as e:
        logger.error(f"❌ Activity logging error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bridge/salary/calculate")
async def log_salary_calculation(salary: SalaryEvent):
    """Log salary calculation to Bucket → Karma pipeline"""
    try:
        logger.info(f"💰 Salary calculation: {salary.user_name} for {salary.month}")
        
        # 1. Write to Bucket
        bucket_payload = {
            "event_type": "salary_calculation",
            "source": "workflow_blackhole",
            "user_id": salary.user_id,
            "user_name": salary.user_name,
            "timestamp": datetime.now().isoformat(),
            "data": {
                "month": salary.month,
                "base_salary": salary.base_salary,
                "hours_worked": salary.hours_worked,
                "overtime_hours": salary.overtime_hours,
                "total_salary": salary.total_salary,
                "metadata": salary.metadata
            }
        }
        
        bucket_success = False
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{PILLARS['bucket']}/core/write-event",
                    json=bucket_payload,
                    timeout=aiohttp.ClientTimeout(total=PILLAR_TIMEOUT)
                ) as resp:
                    bucket_success = resp.status == 200
            except Exception as e:
                logger.warning(f"⚠️ Bucket write failed: {e}")
        
        # 2. Log to Karma (performance-based reward)
        karma_payload = {
            "type": "life_event",
            "data": {
                "user_id": salary.user_id,
                "action": "salary_earned",
                "role": "employee",
                "note": f"Salary for {salary.month}: ${salary.total_salary}",
                "hours_worked": salary.hours_worked
            },
            "source": "workflow_blackhole"
        }
        
        karma_success = False
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{PILLARS['karma']}/v1/event/",
                    json=karma_payload,
                    timeout=aiohttp.ClientTimeout(total=PILLAR_TIMEOUT)
                ) as resp:
                    karma_success = resp.status == 200
            except Exception as e:
                logger.warning(f"⚠️ Karma write failed: {e}")
        
        return {
            "success": True,
            "message": "Salary calculation logged",
            "pillars": {
                "bucket": bucket_success,
                "karma": karma_success
            }
        }
    
    except Exception as e:
        logger.error(f"❌ Salary logging error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bridge/stats")
async def get_bridge_stats():
    """Get bridge statistics"""
    return {
        "service": "workflow_blackhole_bridge",
        "version": "1.0.0",
        "port": 8008,
        "pillars_configured": len(PILLARS),
        "timeout": f"{PILLAR_TIMEOUT}s",
        "endpoints": {
            "attendance": "/bridge/attendance/event",
            "task": "/bridge/task/assign",
            "activity": "/bridge/activity/log",
            "salary": "/bridge/salary/calculate"
        }
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("🌀 Starting Workflow Blackhole Bridge on port 8008...")
    uvicorn.run(app, host="0.0.0.0", port=8008)
