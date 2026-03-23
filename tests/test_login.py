import pytest
import allure
from utils.driver_factory import get_driver
from pages.login_page import LoginPage
from utils.test_data import get_test_cases
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.parametrize("tc", get_test_cases())
@allure.feature("Login Feature")
@allure.story("Login Scenarios")
def test_login(tc, request):   # 👈 add request
    driver = get_driver()
    page = LoginPage(driver)

    try:
        with allure.step("Open login page"):
            driver.get("https://the-internet.herokuapp.com/login")

        with allure.step(f"Login with: {tc['name']}"):
            page.login(tc["username"], tc["password"])

        with allure.step("Validate login result"):
            wait = WebDriverWait(driver, 5)

            try:
                wait.until(EC.url_contains("/secure"))
                actual = "success"
            except:
                actual = "failure"

        # ✅ store actual result for report
        request.node.actual_result = actual

        allure.attach(
            f"Expected: {tc['expected']}, Actual: {actual}",
            name="Result",
            attachment_type=allure.attachment_type.TEXT
        )

        assert actual == tc["expected"]

    except Exception as e:
        request.node.actual_result = "failure"

        allure.attach(
            driver.get_screenshot_as_png(),
            name="Failure Screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        raise e

    finally:
        driver.quit()