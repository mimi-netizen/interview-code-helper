SAMPLE_QUESTIONS = [
    {
        "title": "Two Sum",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "test_cases": """
def test_solution():
    assert solution([2,7,11,15], 9) == [0,1]
    assert solution([3,2,4], 6) == [1,2]
"""
    },
    {
        "title": "Reverse String",
        "description": "Write a function that reverses a string.",
        "test_cases": """
def test_solution():
    assert solution("hello") == "olleh"
    assert solution("world") == "dlrow"
"""
    },
    {
        "title": "Valid Palindrome",
        "description": "Given a string s, return true if it is a palindrome, or false otherwise.",
        "test_cases": """
def test_solution():
    assert solution("A man, a plan, a canal: Panama") == True
    assert solution("race a car") == False
"""
    },
    {
        "title": "Maximum Subarray",
        "description": "Find the contiguous subarray which has the largest sum and return its sum.",
        "test_cases": """
def test_solution():
    assert solution([-2,1,-3,4,-1,2,1,-5,4]) == 6
    assert solution([1]) == 1
"""
    }
]
