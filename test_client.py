import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    # 1. Check API status
    response = requests.get(f"{BASE_URL}/")
    print("API Status:", response.json())

    # 2. Create a test user
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/signup", json=user_data)
    print("\nSignup Response:", response.json())

    # 3. Login with the user
    response = requests.post(f"{BASE_URL}/login", json=user_data)
    print("\nLogin Response:", response.json())
    token = response.json().get("access_token")

    # 4. Get available questions
    response = requests.get(f"{BASE_URL}/questions")
    questions = response.json()
    print("\nAvailable Questions:", json.dumps(questions, indent=2))

    # 5. Submit a solution for the "Reverse String" question
    solution_code = """
def solution(s):
    return s[::-1]
"""
    
    submission = {
        "code": solution_code,
        "question_id": 2,  # ID for "Reverse String" question
        "test_cases": """
def test_solution():
    assert solution("hello") == "olleh"
    assert solution("world") == "dlrow"
"""
    }

    response = requests.post(f"{BASE_URL}/submit", json=submission)
    print("\nSubmission Result:", response.json())

if __name__ == "__main__":
    test_api()
