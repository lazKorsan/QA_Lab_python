import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import time
from robot.api.deco import keyword
from selenium import webdriver
from utils.click_utils import click_utils, ClickUtils
from utils.sendkey_utils import sendKey_utils, SendKeyUtils

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
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'


    @keyword("practicesoftware ana sayfasina gider")
    def go_to_practice_test_homepage(self, browser=None):
        # Kullanıcı global driver nesnesini çeker
        global driver
        # Kullanıcı practice software sayfasına gider
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(practice_software_homePage)
        time.sleep(2)
    @keyword("practicesoftware login sayfasina gider")
    def navigate_to_login_page(self, browser=None):
        global driver
        # Kullanıcı login sayfasına gider
        click_utils(
            driver,
            practice_software_loginButton_Xpath,
            "red"
        )
    @keyword("practice software login islemlerini gerceklestirir")
    def login_procudere(self,email, password):
        global driver
        # Kullanıcı login işlemlerini gerçekleştirir
        # Kullanıcı mailBox kutusuna geçerli mail adresi girer
        sendKey_utils(
            driver,
            practice_software_emailBox_Xpath,
            email
        )

        # Kullanıcı passwordBox kutusuna geçerli password girer
        sendKey_utils(
            driver,
            practice_software_passwordBox_Xpath,
            password
        )

        # Kullanıcı login butonuna tıklar
        click_utils(
            driver,
            practice_software_loginButton_Xpath2,
            "purple",
        )

    @keyword("practicesoftware tarayiciyi kapatir")

    def close_driver(self, browser=None):
        global driver
        if driver:
            driver.quit()

# Kullanım örneği
if __name__ == "__main__":
    practiceSoftWarePage = PracticeSoftWarePage()
    practiceSoftWarePage.go_to_practice_test_homepage()
    practiceSoftWarePage.navigate_to_login_page()
    practiceSoftWarePage.login_procudere(practice_software_email, practice_software_password)
    practiceSoftWarePage.close_driver()
