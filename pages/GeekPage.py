import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import time
from robot.api.deco import keyword
from selenium import webdriver
from utils.click_utils import click_utils, ClickUtils
from utils.sendkey_utils import sendKey_utils, SendKeyUtils

driver = None

geekUrl="https://www.geeksforgeeks.org/"
geekLoginButtonXpath='//button[@class="signinButton gfg_loginModalBtn login-modal-btn"]'
geekMailBoxXpath='//input[@placeholder="Username or Email"]'
geekPasswordBoxXpath='//input[@placeholder="Enter password"]'
geekLoginPageSubmitButtonXpath='//button[@class="loginBtn btnGreen notSocialAuthBtn"]'
geekMail="jemote1577@pazuric.com"
geekPassword="Query.2026!"


class GeekPage:
    
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    # Kullanici geekHomePage sayfasina gider
    @keyword("geekHomePage sayfasina gider")
    def navi_geek_home(self, browser=None):
        global driver
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(geekUrl)
        time.sleep(2)


    # Kullanici geekLoginPage sayfasina gider
    @keyword("geekLoginPage sayfasina gider")
    def navi_geek_login(self, browser=None):
        global driver
        click_utils(
        driver,
        geekLoginButtonXpath,
        "red"
         )
    
    @keyword("login islemlerini gerceklesitirir")
    def geek_login_procudere(self, mail, password):
        # Kullanici login islemlerini gerceklestirir
        global driver
        sendKey_utils(
        driver,
        geekMailBoxXpath,
        mail
        )

    # Kullanici passwordBox kutusuna gecerli password bilgisi girer
        sendKey_utils(
        driver,
        geekPasswordBoxXpath,
        password
        )

    # Kullanici submitButton basarak login olur
        click_utils(
        driver,
        geekLoginPageSubmitButtonXpath,
        "red",
        )
    
    @keyword("tarayiciyi kapatir")
    def close_driver(self, browser=None):
    # Kullanici driver kapatir
         global driver
         if driver :
           driver.quit()


if __name__ == '__main__':
    geekPage=GeekPage()
    geekPage.navi_geek_home()
    geekPage.navi_geek_login()
    geekPage.geek_login_procudere(geekMail, geekPassword)
    geekPage.close_driver()
