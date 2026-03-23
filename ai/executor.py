# ai/executor.py

from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def executor_agent(state):
    driver = state["driver"]
    page = LoginPage(driver)

    results = []
    test_cases = state.get("test_cases", [])

    if not test_cases:
        raise Exception("No test cases found!")

    for tc in test_cases:
        try:
            print(f"\n[Executor] Running: {tc['name']}")

            # Open page
            driver.get("https://the-internet.herokuapp.com/login")

            # Perform login
            page.login(tc["username"], tc["password"])

            # Validate result
            wait = WebDriverWait(driver, 5)

            try:
                wait.until(EC.url_contains("/secure"))
                actual = "success"
            except:
                actual = "failure"

            results.append({
                "name": tc["name"],
                "username": tc["username"],
                "expected": tc["expected"],
                "actual": actual,
                "status": "PASSED" if actual == tc["expected"] else "FAILED"
            })

        except Exception as e:
            print(f"[Executor Error] {tc['name']} → {e}")

            results.append({
                "name": tc["name"],
                "username": tc["username"],
                "expected": tc["expected"],
                "actual": "failure",
                "status": "FAILED",
                "error": str(e)
            })

    return {
        "execution_results": results
    }