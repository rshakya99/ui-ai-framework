from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):

    def login(self, username, password):
        self.driver.find_element(By.ID, "username").clear()
        self.driver.find_element(By.ID, "username").send_keys(username)

        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(password)

        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def get_result(self):
        try:
            return self.driver.find_element(By.ID, "dashboard").is_displayed()
        except:
            return False
