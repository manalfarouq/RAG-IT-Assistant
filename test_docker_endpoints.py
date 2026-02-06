import requests
import time
import sys

BASE_URL = "http://localhost:8000"
EMAIL = "test@example.com"
PASSWORD = "password123"

def print_result(name, success, details=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {name}")
    if details:
        print(f"   {details}")
    if not success:
        sys.exit(1)

def wait_for_api():
    print("Waiting for API to be ready...")
    for _ in range(30):
        try:
            response = requests.get(f"{BASE_URL}/docs")
            if response.status_code == 200:
                print("API is ready!")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    print("API failed to start.")
    sys.exit(1)

def test_register():
    print("\n[1] Testing Registration...")
    payload = {"email": EMAIL, "password": PASSWORD}
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    
    if response.status_code == 201:
        print_result("Register User", True, f"User created: {response.json().get('email')}")
    elif response.status_code == 400 and "existe déjà" in response.text:
         print_result("Register User", True, "User already exists (handled gracefully)")
    else:
        print_result("Register User", False, f"Status: {response.status_code}, Body: {response.text}")

def test_login():
    print("\n[2] Testing Login...")
    payload = {"email": EMAIL, "password": PASSWORD}
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print_result("Login User", True, "Token received")
        return token
    else:
        print_result("Login User", False, f"Status: {response.status_code}, Body: {response.text}")
        return None

def test_get_users(token):
    print("\n[3] Testing Get All Users...")
    # This endpoint is NOT protected according to the router code I saw, but good to check.
    # Actually checking getAllUsers_router.py: @router.get("/", ...) 
    # It has NO security dependency! verify this.
    response = requests.get(f"{BASE_URL}/users/")
    
    if response.status_code == 200:
        users = response.json()
        print_result("Get All Users", True, f"Found {len(users)} users")
    else:
        print_result("Get All Users", False, f"Status: {response.status_code}, Body: {response.text}")

def test_rag_query(token):
    print("\n[4] Testing RAG Query...")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"question": "Test question"}
    
    # query_rag in query_router.py calls pipeline.query.
    # If the pipeline fails (e.g. no PDF, no model), it might 500.
    # But we want to test the endpoint connectivity and auth.
    try:
        response = requests.post(f"{BASE_URL}/query/", json=payload, headers=headers)
        
        if response.status_code == 200:
            answer = response.json().get("answer")
            print_result("RAG Query", True, f"Answer: {answer[:50]}...")
        elif response.status_code == 500:
            # If it fails due to model loading/PDF missing, we still reached the endpoint and passed Auth
            print_result("RAG Query", False, f"Endpoint reached but RAG pipeline failed (Expected if no model/data): {response.text}")
        else:
            print_result("RAG Query", False, f"Status: {response.status_code}, Body: {response.text}")
    except Exception as e:
         print_result("RAG Query", False, f"Exception: {e}")

if __name__ == "__main__":
    wait_for_api()
    test_register()
    token = test_login()
    if token:
        test_get_users(token)
        test_rag_query(token)
