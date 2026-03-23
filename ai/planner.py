import json
import re
from utils.config import llm

def extract_json(text):
    match = re.search(r"\[.*\]", text, re.DOTALL)
    return match.group(0) if match else "[]"

def planner_agent(state):
    scenario = state["scenario"]

    prompt = f"""
    Generate login test cases for:
    {scenario}

    IMPORTANT:
    Only valid credentials:
    username: tomsmith
    password: SuperSecretPassword!

    Any other combination MUST return failure.

    STRICT RULES:
    - Return ONLY valid JSON array
    - No explanation
    - No extra text
    - No JavaScript (.repeat etc.)
    """

    try:
        response = llm.invoke(prompt)
        clean_json = extract_json(response.content)
        test_cases = json.loads(clean_json)
    except Exception as e:
        print("LLM failed:", e)
        print("\u26a0\ufe0f Using fallback test cases")
        test_cases = [
            {"name": "valid login", "username": "tomsmith", "password": "SuperSecretPassword!", "expected": "success"},
            {"name": "invalid password", "username": "tomsmith", "password": "wrong", "expected": "failure"},
            {"name": "invalid username", "username": "wronguser", "password": "SuperSecretPassword!", "expected": "failure"},
            {"name": "both invalid", "username": "wronguser", "password": "wrong", "expected": "failure"},
            {"name": "empty username", "username": "", "password": "SuperSecretPassword!", "expected": "failure"},
            {"name": "empty password", "username": "tomsmith", "password": "", "expected": "failure"},
            {"name": "both empty", "username": "", "password": "", "expected": "failure"},
            {"name": "username special chars", "username": "tom$mith", "password": "SuperSecretPassword!", "expected": "failure"},
            {"name": "password special chars", "username": "tomsmith", "password": "Super$ecret!", "expected": "failure"},
            {"name": "username leading/trailing spaces", "username": " tomsmith ", "password": "SuperSecretPassword!", "expected": "failure"},
            {"name": "password leading/trailing spaces", "username": "tomsmith", "password": " SuperSecretPassword! ", "expected": "failure"},
            {"name": "sql injection username", "username": "' OR '1'='1", "password": "SuperSecretPassword!", "expected": "failure"},
            {"name": "sql injection password", "username": "tomsmith", "password": "' OR '1'='1", "expected": "failure"}
        ]

    # \ud83d\udd25 \ud83d\udd25 ADD THIS VALIDATION (VERY IMPORTANT)
    for tc in test_cases:
        username = tc.get("username", "")
        password = tc.get("password", "")

        if username == "tomsmith" and password == "SuperSecretPassword!":
            tc["expected"] = "success"
        else:
            tc["expected"] = "failure"

    return {"test_cases": test_cases}