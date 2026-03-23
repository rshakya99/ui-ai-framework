import json
from ai.planner import planner_agent

def get_test_cases():
    try:
        state = {"scenario": "Login functionality"}
        result = planner_agent(state)

        if result["test_cases"]:
            return result["test_cases"]

    except Exception as e:
        print("LLM failed:", e)

    # fallback
    print("Using JSON fallback")
    with open("test_data/login.json") as f:
        return json.load(f)