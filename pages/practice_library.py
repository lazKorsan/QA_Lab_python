from robot.api.deco import keyword
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from robot.api.deco import keyword
# from ast import keyword
#from robot.api.deco import keyword
# from pycparser.c_lexer import keyword
# from _ast import keyword


class PracticeLibrary:

    URL = "https://practicesoftwaretesting.com/"

    # ---------- LOCATORS ----------
    LOGIN_NAV = (By.XPATH, '//*[@data-test="nav-sign-in"]')
    EMAIL_BOX = (By.ID, "email")
    PASS_BOX = (By.ID, "password")
    LOGIN_BTN = (By.XPATH, '//input[@data-test="login-submit"]')

    # ---------- INIT ----------
    def __init__(self):
        self.driver = None
        self.wait = None

    # ---------- INTERNAL ----------
    def _start_driver(self, browser="chrome"):
        if browser.lower() == "chrome":
            self.driver = webdriver.Chrome()
        else:
            raise ValueError("Only Chrome is supported for now.")

        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def _wait_and_click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def _wait_and_type(self, locator, text):
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    # ---------- ROBOT KEYWORDS ----------
    @keyword("Go To Home")
    def go_to_home(self, browser="chrome"):
        """
        Robot Keyword: Go To Home
        """
        if not self.driver:
            self._start_driver(browser)

        self.driver.get(self.URL)
    @keyword("Go To Login")
    def go_to_login(self):
        """
        Robot Keyword: Go To Login
        """
        self._wait_and_click(self.LOGIN_NAV)
        # ###

    @keyword("Login")
    def login(self, email, password):
        """
        Robot Keyword: Login
        """
        self._wait_and_type(self.EMAIL_BOX, email)
        self._wait_and_type(self.PASS_BOX, password)
        self._wait_and_click(self.LOGIN_BTN)

    @keyword("Quit Driver")
    def quit_driver(self):
        """
        Robot Keyword: Quit Driver
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.wait = None