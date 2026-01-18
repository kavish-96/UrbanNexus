
import requests
import sys

BASE_URL = "http://localhost:8000/api"

def check(name, result, context=""):
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{status} - {name} {context}")
    if not result:
        sys.exit(1)

def validate_system():
    print("--- 🔍 Sytem Validation Started ---")
    
    # 1. Test Dashboard Data (Read)
    try:
        print("\n1. Testing Dashboard API (GET /dashboard/?city_id=2)...")
        resp = requests.get(f"{BASE_URL}/dashboard/?city_id=2")
        check("Status Code 200", resp.status_code == 200)
        
        data = resp.json()
        stats = data.get("latest_stats", {})
        
        check("City Name is Delhi", data.get("city") == "Delhi")
        check("Has Temperature", stats.get("temperature") is not None, f"(Value: {stats.get('temperature')})")
        check("Has Rainfall", "rainfall" in stats, f"(Value: {stats.get('rainfall')})")
        check("Has Health Risk", stats.get("health_risk") is not None, f"(Value: {stats.get('health_risk')})")
        
    except Exception as e:
        check("Dashboard API Failed", False, str(e))

    # 2. Test Live Sync (Write + Logic)
    try:
        print("\n2. Testing Live Weather Sync (POST /sync/weather/)...")
        resp = requests.post(f"{BASE_URL}/sync/weather/")
        check("Status Code 200", resp.status_code == 200)
        
        result = resp.json()
        check("Sync Response has 'success'", "success" in result)
        print(f"   Response: {result['success'][1] if len(result['success']) > 1 else result}")

    except Exception as e:
        check("Sync API Failed", False, str(e))
        
    print("\n--- 🎉 All Systems Go! ---")

if __name__ == "__main__":
    validate_system()
