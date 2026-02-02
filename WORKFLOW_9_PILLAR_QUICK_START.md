# 🚀 9-Pillar Quick Start Guide

**Workflow Blackhole Integration Complete**

---

## 📋 Prerequisites

All 8 existing pillars must be running:
- ✅ Karma (8000)
- ✅ Bucket (8001)
- ✅ Core (8002)
- ✅ Workflow Executor (8003)
- ✅ UAO (8004)
- ✅ Insight Core (8005)
- ✅ Insight Flow Bridge (8006)
- ✅ Insight Flow Backend (8007) - Optional

---

## 🔧 Setup (One-time)

### 1. Install Bridge Dependencies
```bash
cd "workflow-blackhole-main\bridge"
pip install -r requirements.txt
```

### 2. Configure Environment
Add to `workflow-blackhole-main\server\.env`:
```env
# Pillar Integration
BRIDGE_URL=http://localhost:8008
PILLAR_INTEGRATION_ENABLED=true
```

---

## 🚀 Starting the System

### Start All 8 Pillars First
Follow the main README.md to start services on ports 8000-8007.

### Step 9: Start Workflow Bridge (Terminal 9)
```bash
cd "workflow-blackhole-main\bridge"
start_bridge.bat
```
✅ Wait for: "Uvicorn running on http://0.0.0.0:8008"  
✅ Bridge runs on: **http://localhost:8008**  
✅ Health check: `curl http://localhost:8008/health`

### Step 10: Start Workflow Backend (Terminal 10)
```bash
cd "workflow-blackhole-main\server"
npm start
```
✅ Wait for: "Server running on port 5001"  
✅ Backend runs on: **http://localhost:5001**

### Step 11: Start Workflow Frontend (Terminal 11)
```bash
cd "workflow-blackhole-main\client"
npm run dev
```
✅ Wait for: "Local: http://localhost:5173"  
✅ Frontend runs on: **http://localhost:5173**

---

## 🧪 Testing Integration

### Quick Test
```bash
python test_9_pillar_integration.py
```

Expected: **5/5 tests passing (100%)**
- ✅ Health Checks (9 services)
- ✅ Attendance Flow (Bridge → Bucket → Karma)
- ✅ Task Assignment (AI routing via Core + Insight Flow)
- ✅ Activity Logging (PRANA pipeline)
- ✅ Bridge Statistics

---

## 📊 Port Assignments

| Service | Port | Status | Required |
|---------|------|--------|----------|
| Karma | 8000 | ✅ Running | Yes |
| Bucket | 8001 | ✅ Running | Yes |
| Core | 8002 | ✅ Running | Yes |
| Workflow Executor | 8003 | ✅ Running | Yes |
| UAO | 8004 | ✅ Running | Yes |
| Insight Core | 8005 | ✅ Running | Yes |
| Insight Flow Bridge | 8006 | ✅ Running | Yes |
| Insight Flow Backend | 8007 | ⚠️ Optional | No |
| **Workflow Bridge** | **8008** | **✅ Running** | **Yes** |
| Workflow Backend | 5001 | ✅ Running | Yes |
| Workflow Frontend | 5173 | ✅ Running | Yes |

---

## 🔄 Data Flow Examples

### Attendance Event
```
Employee starts day (Frontend)
    ↓
Workflow Backend (5001)
    ↓
Workflow Bridge (8008)
    ↓
Bucket (8001) - Audit trail
    ↓
Karma (8000) - Behavioral tracking
```

### Task Assignment
```
Admin creates task (Frontend)
    ↓
Workflow Backend (5001)
    ↓
Workflow Bridge (8008)
    ↓
Insight Flow (8006) - Agent routing
    ↓
Core (8002) - AI processing
    ↓
Bucket (8001) - Event logging
```

### Employee Activity
```
Screen capture (Frontend)
    ↓
Workflow Backend (5001)
    ↓
Workflow Bridge (8008)
    ↓
PRANA packet → Bucket (8001)
    ↓
Karma (8000) - Cognitive analysis
```

---

## 🎯 Integration Features

### ✅ Implemented
- Fire-and-forget pillar calls (2s timeout)
- Attendance event logging (Bucket + Karma)
- Task AI routing (Core + Insight Flow)
- Employee activity tracking (PRANA)
- Salary calculation logging
- Graceful degradation (works if pillars down)
- Complete audit trail
- Behavioral scoring

### ⏳ Optional Enhancements
- JWT validation via Insight Core
- Real-time Socket.IO integration
- Advanced analytics dashboard
- Performance metrics tracking

---

## 🔍 Monitoring

### Check Bridge Health
```bash
curl http://localhost:8008/health
```

### Check Bridge Stats
```bash
curl http://localhost:8008/bridge/stats
```

### Check Pillar Integration
```bash
# Bucket events
curl http://localhost:8001/core/events

# Karma profile
curl http://localhost:8000/api/v1/karma/test_user_123

# PRANA packets
curl http://localhost:8001/bucket/prana/packets?limit=10
```

---

## 🎉 Success Indicators

✅ All 9 services running (8 pillars + bridge)  
✅ Bridge health check returns all pillars  
✅ Attendance events logged to Bucket + Karma  
✅ Tasks routed through AI (Core + Insight Flow)  
✅ Employee activity tracked via PRANA  
✅ Zero regression in Workflow Blackhole  
✅ Graceful degradation operational  
✅ Complete audit trail in Bucket  
✅ 9-pillar test passes 5/5 (100%)  

**The 9th pillar (Model Layer) is now integrated! 🌀**

---

## 📚 Documentation

- **WORKFLOW_BLACKHOLE_INTEGRATION.md** - Complete integration guide
- **README.md** - Main system documentation (updated for 9 pillars)
- **workflow_bridge.py** - Bridge service source code
- **pillar_client.js** - Node.js integration client

---

**Last Updated**: 2026-01-31  
**Status**: ✅ Integration Complete
