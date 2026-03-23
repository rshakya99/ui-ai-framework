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

    response = llm.invoke(prompt)

    try:
        clean_json = extract_json(response.content)
        test_cases = json.loads(clean_json)
    except Exception as e:
        print("JSON PARSE ERROR:", e)
        test_cases = []

    # ✅ FALLBACK
    if not test_cases:
        print("⚠️ Using fallback test cases")

        test_cases = [
            {
                "name": "valid login",
                "username": "tomsmith",
                "password": "SuperSecretPassword!",
                "expected": "success"
            },
            {
                "name": "invalid login",
                "username": "tomsmith",
                "password": "wrong",
                "expected": "failure"
            }
        ]

    # 🔥 🔥 ADD THIS VALIDATION (VERY IMPORTANT)
    for tc in test_cases:
        username = tc.get("username", "")
        password = tc.get("password", "")

        if username == "tomsmith" and password == "SuperSecretPassword!":
            tc["expected"] = "success"
        else:
            tc["expected"] = "failure"

    return {"test_cases": test_cases}