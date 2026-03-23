class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def click(self, element):
        element.click()

    def enter_text(self, element, text):
        element.clear()
        element.send_keys(text)
