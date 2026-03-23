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

    # fallback to hardcoded test cases from planner_agent
    print("Using hardcoded fallback test cases")
    return planner_agent({"scenario": "Login functionality"})["test_cases"]
