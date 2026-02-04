#!/usr/bin/env python3
"""
BHIV Bucket Health Check Script
Tests all critical endpoints after deployment
"""

import requests
import json
import sys
import time
from datetime import datetime

def health_check(base_url):
    """Comprehensive health check for BHIV Bucket service"""
    
    print(f"🏥 Health Check for BHIV Bucket")
    print(f"🌐 Base URL: {base_url}")
    print(f"⏰ Time: {datetime.now().isoformat()}")
    print("=" * 50)
    
    tests = [
        {
            "name": "Service Health",
            "endpoint": "/health",
            "method": "GET",
            "expected_status": 200,
            "required_fields": ["status", "bucket_version"]
        },
        {
            "name": "Agents List",
            "endpoint": "/agents",
            "method": "GET", 
            "expected_status": 200
        },
        {
            "name": "Baskets List",
            "endpoint": "/baskets",
            "method": "GET",
            "expected_status": 200,
            "required_fields": ["baskets", "count"]
        },
        {
            "name": "Redis Status",
            "endpoint": "/redis/status",
            "method": "GET",
            "expected_status": [200, 503]  # 503 is OK if Redis not connected
        },
        {
            "name": "Core Integration Stats",
            "endpoint": "/core/stats",
            "method": "GET",
            "expected_status": 200,
            "required_fields": ["stats", "integration_status"]
        },
        {
            "name": "PRANA Stats",
            "endpoint": "/bucket/prana/stats",
            "method": "GET",
            "expected_status": 200,
            "required_fields": ["stats", "telemetry_status"]
        },
        {
            "name": "Governance Info",
            "endpoint": "/governance/info",
            "method": "GET",
            "expected_status": 200
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            print(f"🧪 Testing: {test['name']}")
            
            url = f"{base_url}{test['endpoint']}"
            response = requests.get(url, timeout=10)
            
            # Check status code
            expected_status = test['expected_status']
            if isinstance(expected_status, list):
                status_ok = response.status_code in expected_status
            else:
                status_ok = response.status_code == expected_status
            
            if not status_ok:
                print(f"   ❌ Status: {response.status_code} (expected {expected_status})")
                failed += 1
                continue
            
            # Check required fields if specified
            if 'required_fields' in test and response.status_code == 200:
                try:
                    data = response.json()
                    missing_fields = []
                    for field in test['required_fields']:
                        if field not in data:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        print(f"   ❌ Missing fields: {missing_fields}")
                        failed += 1
                        continue
                except json.JSONDecodeError:
                    print(f"   ❌ Invalid JSON response")
                    failed += 1
                    continue
            
            print(f"   ✅ Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'status' in data:
                        print(f"   📊 Service Status: {data['status']}")
                except:
                    pass
            
            passed += 1
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
            failed += 1
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            failed += 1
        
        print()
    
    print("=" * 50)
    print(f"📊 Health Check Results:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("🎉 All health checks passed! Service is healthy.")
        return True
    else:
        print("⚠️  Some health checks failed. Check service configuration.")
        return False

def test_core_integration(base_url):
    """Test Core integration endpoints"""
    print("\n🔗 Testing Core Integration...")
    
    # Test write event
    try:
        response = requests.post(f"{base_url}/core/write-event", json={
            "requester_id": "bhiv_core",
            "event_data": {
                "event_type": "health_check",
                "agent_id": "test_agent",
                "message": "Health check test event"
            }
        }, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Core event write successful")
        else:
            print(f"   ❌ Core event write failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Core integration test failed: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python health_check.py <base_url>")
        print("Example: python health_check.py https://your-service.onrender.com")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    # Run health checks
    healthy = health_check(base_url)
    
    # Test integrations
    test_core_integration(base_url)
    
    # Exit with appropriate code
    sys.exit(0 if healthy else 1)

if __name__ == "__main__":
    main()