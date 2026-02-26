import time
from selenium import webdriver
from utils.click_utils import click_utils
from utils.sendkey_utils import sendKey_utils

# Global driver nesnesi
driver = None

# Xpath ve diğer değişkenler
practice_software_loginButton_Xpath = '//*[@data-test="nav-sign-in"]'
practice_software_emailBox_Xpath = '//input[@id="email"]'
practice_software_passwordBox_Xpath = '//input[@id="password"]'
practice_software_loginButton_Xpath2 = '//input[@data-test="login-submit"]'
practice_software_homePage = "https://practicesoftwaretesting.com/"
practice_software_email = "lazKorsan123@gmail.com"
practice_software_password = "Query.2026"

class PracticeSoftWarePage:

    @staticmethod
    def go_to_practice_test_homepage():
        # Kullanıcı global driver nesnesini çeker
        global driver
        # Kullanıcı practice software sayfasına gider
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(practice_software_homePage)
        time.sleep(2)

    @staticmethod
    def navigate_to_login_page():
        global driver
        # Kullanıcı login sayfasına gider
        click_utils(
            driver,
            practice_software_loginButton_Xpath,
            "red"
        )

    @staticmethod
    def login_procudere(email, password):
        global driver
        # Kullanıcı login işlemlerini gerçekleştirir
        # Kullanıcı mailBox kutusuna geçerli mail adresi girer
        sendKey_utils(
            driver,
            practice_software_emailBox_Xpath,
            email,
            "true",
        )

        # Kullanıcı passwordBox kutusuna geçerli password girer
        sendKey_utils(
            driver,
            practice_software_passwordBox_Xpath,
            password,
            "true",
        )

        # Kullanıcı login butonuna tıklar
        click_utils(
            driver,
            practice_software_loginButton_Xpath2,
            "purple",
        )

    @staticmethod
    def close_driver():
        global driver
        if driver:
            driver.quit()

# Kullanım örneği
if __name__ == "__main__":
    page = PracticeSoftWarePage()
    page.go_to_practice_test_homepage()
    page.navigate_to_login_page()
    page.login_procudere(practice_software_email, practice_software_password)
    page.close_driver()
