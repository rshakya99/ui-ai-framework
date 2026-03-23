# conftest.py

from utils.report import generate_excel

all_results = []

def pytest_runtest_makereport(item, call):
    if call.when == "call":
        tc = {}

        # Get test case data (from parametrize)
        if hasattr(item, "callspec"):
            tc = item.callspec.params.get("tc", {})

        result = {
            "test_name": item.name,
            "description": tc.get("name", ""),
            "username": tc.get("username", ""),
            "expected": tc.get("expected", ""),
            "actual": getattr(item, "actual_result", ""),
            "status": "PASSED" if call.excinfo is None else "FAILED"
        }

        all_results.append(result)


def pytest_sessionfinish(session, exitstatus):
    generate_excel(all_results)