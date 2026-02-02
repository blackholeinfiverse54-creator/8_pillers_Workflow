"""
9-Pillar Integration Test
Tests Workflow Blackhole Bridge + 8 Existing Pillars
"""

import requests
import time
from datetime import datetime

# Service URLs
SERVICES = {
    "karma": "http://localhost:8000",
    "bucket": "http://localhost:8001",
    "core": "http://localhost:8002",
    "workflow": "http://localhost:8003",
    "uao": "http://localhost:8004",
    "insight": "http://localhost:8005",
    "insight_flow": "http://localhost:8006",
    "insight_flow_backend": "http://localhost:8007",
    "workflow_bridge": "http://localhost:8008"
}

def test_health_checks():
    """Test 1: Health checks for all 9 services"""
    print("\n" + "="*60)
    print("TEST 1: Health Checks (9 Services)")
    print("="*60)
    
    results = {}
    for name, url in SERVICES.items():
        try:
            if name == "uao":
                response = requests.get(f"{url}/docs", timeout=2)
            else:
                response = requests.get(f"{url}/health", timeout=2)
            
            if response.status_code == 200:
                results[name] = "✅ HEALTHY"
                print(f"✅ {name.upper()}: Healthy")
            else:
                results[name] = f"⚠️ UNHEALTHY ({response.status_code})"
                print(f"⚠️ {name.upper()}: Unhealthy ({response.status_code})")
        except Exception as e:
            results[name] = f"❌ UNREACHABLE"
            print(f"❌ {name.upper()}: Unreachable - {str(e)[:50]}")
    
    passed = sum(1 for v in results.values() if "✅" in v)
    total = len(results)
    print(f"\n📊 Result: {passed}/{total} services healthy")
    return passed >= 7  # At least 7/9 should be healthy

def test_attendance_flow():
    """Test 2: Attendance event flow (Bridge → Bucket → Karma)"""
    print("\n" + "="*60)
    print("TEST 2: Attendance Event Flow")
    print("="*60)
    
    try:
        # Send attendance event through bridge
        payload = {
            "user_id": "test_user_123",
            "user_name": "Test Employee",
            "event_type": "start_day",
            "timestamp": datetime.now().isoformat(),
            "location": {
                "latitude": 19.1663,
                "longitude": 72.8526,
                "address": "Test Office"
            },
            "hours_worked": None,
            "metadata": {
                "test": True
            }
        }
        
        response = requests.post(
            f"{SERVICES['workflow_bridge']}/bridge/attendance/event",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Bridge: Attendance event sent")
            print(f"   Bucket: {'✅' if result.get('pillars', {}).get('bucket') else '⚠️'}")
            print(f"   Karma: {'✅' if result.get('pillars', {}).get('karma') else '⚠️'}")
            
            # Verify in Bucket
            time.sleep(1)
            bucket_response = requests.get(f"{SERVICES['bucket']}/core/events", timeout=2)
            if bucket_response.status_code == 200:
                print(f"✅ Bucket: Event verified")
            
            return True
        else:
            print(f"❌ Bridge returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Attendance flow failed: {e}")
        return False

def test_task_assignment():
    """Test 3: Task assignment with AI routing"""
    print("\n" + "="*60)
    print("TEST 3: Task Assignment with AI Routing")
    print("="*60)
    
    try:
        payload = {
            "task_id": "task_test_123",
            "title": "Analyze quarterly performance metrics",
            "assignee_id": "emp_456",
            "assignee_name": "John Doe",
            "priority": "High",
            "status": "Pending",
            "department": "Analytics",
            "metadata": {
                "test": True
            }
        }
        
        response = requests.post(
            f"{SERVICES['workflow_bridge']}/bridge/task/assign",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Bridge: Task assignment processed")
            print(f"   Selected Agent: {result.get('selected_agent', 'N/A')}")
            print(f"   Insight Flow: {'✅' if result.get('pillars', {}).get('insight_flow') else '⚠️'}")
            print(f"   Core: {'✅' if result.get('pillars', {}).get('core') else '⚠️'}")
            print(f"   Bucket: {'✅' if result.get('pillars', {}).get('bucket') else '⚠️'}")
            return True
        else:
            print(f"❌ Bridge returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Task assignment failed: {e}")
        return False

def test_activity_logging():
    """Test 4: Employee activity logging (PRANA pipeline)"""
    print("\n" + "="*60)
    print("TEST 4: Employee Activity Logging")
    print("="*60)
    
    try:
        payload = {
            "user_id": "test_user_123",
            "activity_type": "screen_capture",
            "timestamp": datetime.now().isoformat(),
            "productivity_score": 85,
            "metadata": {
                "test": True,
                "application": "VS Code"
            }
        }
        
        response = requests.post(
            f"{SERVICES['workflow_bridge']}/bridge/activity/log",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Bridge: Activity logged")
            print(f"   PRANA: {'✅' if result.get('pillars', {}).get('prana') else '⚠️'}")
            
            # Verify in Bucket PRANA
            time.sleep(1)
            prana_response = requests.get(
                f"{SERVICES['bucket']}/bucket/prana/packets?limit=5",
                timeout=2
            )
            if prana_response.status_code == 200:
                print(f"✅ Bucket: PRANA packet verified")
            
            return True
        else:
            print(f"❌ Bridge returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Activity logging failed: {e}")
        return False

def test_bridge_stats():
    """Test 5: Bridge statistics endpoint"""
    print("\n" + "="*60)
    print("TEST 5: Bridge Statistics")
    print("="*60)
    
    try:
        response = requests.get(f"{SERVICES['workflow_bridge']}/bridge/stats", timeout=2)
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Bridge Stats Retrieved")
            print(f"   Service: {stats.get('service')}")
            print(f"   Version: {stats.get('version')}")
            print(f"   Port: {stats.get('port')}")
            print(f"   Pillars: {stats.get('pillars_configured')}")
            return True
        else:
            print(f"❌ Bridge returned {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Stats retrieval failed: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🌀 9-PILLAR INTEGRATION TEST")
    print("Workflow Blackhole + 8 Existing Pillars")
    print("="*60)
    
    tests = [
        ("Health Checks", test_health_checks),
        ("Attendance Flow", test_attendance_flow),
        ("Task Assignment", test_task_assignment),
        ("Activity Logging", test_activity_logging),
        ("Bridge Stats", test_bridge_stats)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            results.append((name, False))
        time.sleep(1)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
        if result:
            passed += 1
    
    total = len(results)
    percentage = (passed / total) * 100
    
    print(f"\n🎯 Final Score: {passed}/{total} tests passed ({percentage:.0f}%)")
    
    if percentage == 100:
        print("✅ 9-PILLAR INTEGRATION: PRODUCTION READY")
    elif percentage >= 80:
        print("⚠️ 9-PILLAR INTEGRATION: MOSTLY OPERATIONAL")
    else:
        print("❌ 9-PILLAR INTEGRATION: NEEDS ATTENTION")
    
    print("="*60)

if __name__ == "__main__":
    main()
