import sys
import os

from robot.api.deco import keyword

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import time
from selenium import webdriver
from utils.click_utils import click_utils
from utils.sendkey_utils import sendKey_utils

driver = None


loyalUrl="https://qa.loyalfriendcare.com/en"
loyalmail="lazKorsan190220262054@gmail.com"
loyalpassword="Query.2026!"
loyalLoginButtonXpath='//*[@class="btn_add"]'
loyalMailBoxXpath='//input[@id="email"]'
loyalPasswordBoxXpath='//input[@id="password"]'
loyalSubmitButtonXpath='//button[@class="btn btn-primary btn-cons m-t-10"]'


class LoyalFriendCarePage:
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    @keyword("loyalFriendCare sayfasina gider")
    def navi_loyal_home(self, browser=None):
        global driver
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(loyalUrl)
        time.sleep(2)


    @keyword("loyalfriendCareLogin sayfasina gider")
    def navi_loyal_login(self, browser=None):
        global driver
        click_utils(
        driver,
        loyalLoginButtonXpath,
        "red"
         )

    @keyword("loyalfriendCare login islemlerini gerceklesitirir")
    def loyal_login_procudere(self, mail, password):
        # Kullanici login islemlerini gerceklestirir
        global driver
        sendKey_utils(
        driver,
        loyalMailBoxXpath,
        mail
            )

    # Kullanici passwordBox kutusuna gecerli password bilgisi girer
        sendKey_utils(
            driver,
        loyalPasswordBoxXpath,
        password
            )

    # Kullanici submitButton basarak login olur
        click_utils(
        driver,
        loyalSubmitButtonXpath,
        "red",

        )

    @keyword("loyalfriendCare tarayiciyi kapatir")
    def close_driver(self, browser=None):
        global driver
        if driver :
            driver.quit()

if __name__ == "__main__":
    loyalFriendCarePage=LoyalFriendCarePage()
    loyalFriendCarePage.navi_loyal_home()
    loyalFriendCarePage.navi_loyal_login()
    loyalFriendCarePage.loyal_login_procudere(loyalmail, loyalpassword)
    loyalFriendCarePage.close_driver()
