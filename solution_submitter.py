import requests
import json
import sys

class InterviewCoderClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        self.headers = {"Content-Type": "application/json"}

    def login(self, email, password):
        response = requests.post(
            f"{self.base_url}/login",
            json={"email": email, "password": password},
            headers=self.headers
        )
        data = response.json()
        self.token = data.get("access_token")
        return data

    def get_questions(self):
        response = requests.get(f"{self.base_url}/questions")
        return response.json()

    def submit_solution(self, question_id, solution_code):
        # Get the question to access its test cases
        questions = self.get_questions()
        question = next((q for q in questions["questions"] if q["id"] == question_id), None)
        
        if not question:
            print(f"Question {question_id} not found!")
            return

        submission = {
            "code": solution_code,
            "question_id": question_id,
            "test_cases": question["test_cases"]
        }

        response = requests.post(
            f"{self.base_url}/submit",
            json=submission,
            headers=self.headers
        )
        return response.json()

def main():
    client = InterviewCoderClient()
    
    # Sample solutions
    solutions = {
        # Two Sum solution
        1: """
def solution(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
""",
        # Reverse String solution
        2: """
def solution(s):
    return s[::-1]
"""
    }

    # Login
    print("Logging in...")
    client.login("user@example.com", "mypassword123")

    # Get questions
    print("\nAvailable questions:")
    questions = client.get_questions()
    for q in questions["questions"]:
        print(f"{q['id']}. {q['title']}")

    # Submit solutions
    for question_id, solution_code in solutions.items():
        print(f"\nSubmitting solution for question {question_id}...")
        result = client.submit_solution(question_id, solution_code)
        print(f"Result: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    main()
