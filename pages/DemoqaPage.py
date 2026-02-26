import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import time
from robot.api.deco import keyword
from selenium import webdriver
from utils.click_utils import click_utils, ClickUtils
from utils.sendkey_utils import sendKey_utils, SendKeyUtils

driver = None

demoqaUserNmaeBoxXpath='//input[@id="userName"]'
demoqaPasswordBoxXpath='//input[@id="password"]'
demoqaSingInButtonXpath="//button[@id='login']"
demoqaUserName="lazKorsan"
demoqaPassword="Query.2026!"

class DemoqaPage:
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    @keyword("demoqa ana sayfasina gider")
    def navi_demoqa_home(self, browser=None):
        global driver
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://demoqa.com/")
        time.sleep(2)

    @keyword("demoqa login sayfasina gider")
    def navi_demoqa_login(self, browser=None):
        global driver
        driver.get("https://demoqa.com/login")

    @keyword("login islemlerini gerceklesitirir")
    def demoqa_login_procudure(self,userName, password):
        global driver
        sendKey_utils(
        driver,
        demoqaUserNmaeBoxXpath,
        userName
        )


        sendKey_utils(
        driver,
        demoqaPasswordBoxXpath,
        password
        )

        click_utils(
        driver,
        demoqaSingInButtonXpath
        )

    @keyword("demoqa tarayiciyi kapatir")
    def close_driver(self, browser=None):
        global driver
        if driver :
            driver.quit()

if __name__ == '__main__':
    demoqaPage=DemoqaPage()
    demoqaPage.navi_demoqa_home()
    demoqaPage.navi_demoqa_login()
    demoqaPage.demoqa_login_procudure(demoqaUserName,demoqaPassword)
    demoqaPage.close_driver()

