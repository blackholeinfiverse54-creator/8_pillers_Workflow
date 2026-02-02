# 🚀 BHIV AI Platform: 8-Pillar Infrastructure + Model Layers

**Status**: ✅ **PRODUCTION READY** | **Architecture**: 8 Pillars + Layer 1 (Workforce Management)  
**Last Updated**: 2026-02-02 | **Version**: 3.0.0

---

## 🎯 System Architecture

### 8-Pillar Infrastructure (Foundation)
Reusable core services that power all model layers:

| Pillar | Port | Purpose |
|--------|------|---------|
| **Karma** | 8000 | Q-learning behavioral tracking & karma computation |
| **Bucket** | 8001 | Constitutional governance, audit trail & event storage |
| **Core** | 8002 | AI Decision Engine with UCB-based agent selection |
| **Workflow Executor** | 8003 | Deterministic action execution |
| **UAO** | 8004 | Unified action orchestration & lifecycle management |
| **Insight Core** | 8005 | JWT security & replay attack prevention |
| **Insight Flow** | 8006/8007 | Intelligent agent routing with Q-learning |
| **PRANA** | Frontend | User behavior telemetry & cognitive state tracking |

### Model Layers (Built on 8 Pillars)
Business applications that leverage the infrastructure:

**✅ Layer 1: Workflow Blackhole (Workforce Management)**
- **Bridge**: Port 8008 (Integration layer)
- **Backend**: Port 5001 (Node.js/Express + MongoDB)
- **Frontend**: Port 5173 (React + Vite)
- **Features**: Attendance tracking, task management, salary calculation, employee monitoring, leave management
- **Integration**: Fire-and-forget pattern with all 8 pillars
- **Status**: Production ready

**🔮 Future Layers**:
- Layer 2: HR Management System
- Layer 3: Customer Relationship Management (CRM)
- Layer 4: Project Management System
- Layer 5: Inventory Management
- Layer 6: Financial Management

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│         LAYER 1: WORKFLOW BLACKHOLE (Workforce Mgmt)        │
│   Frontend (5173) → Backend (5001) → Bridge (8008)          │
│   Features: Attendance, Tasks, Salary, Monitoring, Leave    │
└────────────────────────────┬────────────────────────────────┘
                             ↓ (fire-and-forget)
┌─────────────────────────────────────────────────────────────┐
│                  8-PILLAR INFRASTRUCTURE                     │
├─────────────────────────────────────────────────────────────┤
│  Karma (8000)         → Behavioral tracking                  │
│  Bucket (8001)        → Audit trail & storage                │
│  Core (8002)          → AI processing                        │
│  Workflow (8003)      → Action execution                     │
│  UAO (8004)           → Orchestration                        │
│  Insight Core (8005)  → Security                             │
│  Insight Flow (8006)  → Intelligent routing                  │
│  PRANA (Frontend)     → User telemetry                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Start 8-Pillar Infrastructure

```bash
# Terminal 1: Karma
cd karma_chain_v2-main && python main.py

# Terminal 2: Bucket
cd BHIV_Central_Depository-main && python main.py

# Terminal 3: Core
cd v1-BHIV_CORE-main && python mcp_bridge.py

# Terminal 4: Workflow Executor
cd workflow-executor-main && python main.py

# Terminal 5: UAO
cd "Unified Action Orchestration" && python action_orchestrator.py

# Terminal 6: Insight Core
cd insightcore-bridgev4x-main && python insight_service.py

# Terminal 7: Insight Flow
cd Insight_Flow-main && start_bridge_standalone.bat

# Terminal 8: Insight Flow Backend (Optional)
cd Insight_Flow-main && start_insight_flow_fixed.bat
```

### Start Layer 1: Workflow Blackhole

```bash
# Terminal 9: Bridge
cd workflow-blackhole-main\bridge && python workflow_bridge.py

# Terminal 10: Backend
cd workflow-blackhole-main\server && npm start

# Terminal 11: Frontend
cd workflow-blackhole-main\client && npm run dev
```

**Access**: http://localhost:5173

---

## 📊 Port Assignments

| Service | Port | Type | Status |
|---------|------|------|--------|
| Karma | 8000 | Pillar | ✅ Running |
| Bucket | 8001 | Pillar | ✅ Running |
| Core | 8002 | Pillar | ✅ Running |
| Workflow Executor | 8003 | Pillar | ✅ Running |
| UAO | 8004 | Pillar | ✅ Running |
| Insight Core | 8005 | Pillar | ✅ Running |
| Insight Flow Bridge | 8006 | Pillar | ✅ Running |
| Insight Flow Backend | 8007 | Pillar | Optional |
| **Workflow Bridge** | **8008** | **Layer 1** | **✅ Running** |
| **Workflow Backend** | **5001** | **Layer 1** | **✅ Running** |
| **Workflow Frontend** | **5173** | **Layer 1** | **✅ Running** |

---

## 🔄 Integration Flow

### Layer 1 → 8 Pillars

**Attendance Event**:
```
Employee → Frontend (5173) → Backend (5001) → Bridge (8008)
    ↓
Bucket (8001) - Audit trail
    ↓
Karma (8000) - Behavioral scoring
```

**Task Assignment**:
```
Admin → Frontend (5173) → Backend (5001) → Bridge (8008)
    ↓
Insight Flow (8006) - Agent routing
    ↓
Core (8002) - AI processing
    ↓
Bucket (8001) - Event logging
```

**Employee Activity**:
```
Activity → Frontend (5173) → Backend (5001) → Bridge (8008)
    ↓
PRANA packet → Bucket (8001)
    ↓
Karma (8000) - Cognitive analysis
```

---

## ✅ Success Indicators

**8-Pillar Infrastructure**:
- ✅ All 8 services running
- ✅ Health checks passing
- ✅ Integration tests: 8/8 (100%)

**Layer 1 (Workflow Blackhole)**:
- ✅ Bridge connected to all pillars
- ✅ Backend connected to MongoDB
- ✅ Frontend accessible
- ✅ Fire-and-forget pattern working
- ✅ Graceful degradation active

---

## 📚 Documentation

- **WORKFLOW_BLACKHOLE_INTEGRATION.md** - Layer 1 technical guide
- **WORKFLOW_9_PILLAR_QUICK_START.md** - Quick start for Layer 1
- **WORKFLOW_PRODUCTION_READY.md** - Production configuration
- **COMPREHENSIVE_ARCHITECTURE_ANALYSIS.md** - Complete system architecture
- **QUICK_REFERENCE.md** - Quick commands

---

## 🎯 Key Features

✅ **Scalable Architecture**: Multiple layers can run simultaneously  
✅ **Fire-and-Forget Integration**: Non-blocking async operations  
✅ **Graceful Degradation**: Layers work independently  
✅ **Complete Audit Trail**: Every action logged permanently  
✅ **Security Layer**: JWT validation + replay attack prevention  
✅ **RL Intelligence**: Q-learning behavioral tracking  
✅ **Production Ready**: 100% test pass rate  

---

**Last Updated**: 2026-02-02  
**Maintained By**: Ashmit Pandey  
**Status**: Production Ready ✅
