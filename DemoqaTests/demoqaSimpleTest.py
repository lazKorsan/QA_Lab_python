import time

from selenium import webdriver

from utils.click_utils import click_utils
from utils.sendkey_utils import sendKey_utils

demoqaUserNmaeBoxXpath='//input[@id="userName"]'
demoqaPasswordBoxXpath='//input[@id="password"]'
demoqaSingInButtonXpath="//button[@id='login']"
demoqaUserName="lazKorsan"
demoqaPassword="Query.2026!"


def test_demoqa_simple_tests():
    # todo bu test daha sonra kullanılmaz hale gelebilri
    #  demoqa aralıklarla kullanıcı siliyor olabilir

    # demoqa kullanicisi ana sayfaya gider
    driver=webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://demoqa.com/")
    time.sleep(2)

    # demoqa kullanicisi login page e gider
    driver.get("https://demoqa.com/login")

    # demoqa kullanicisi userNameBox a isim girer
    sendKey_utils(
        driver,
        demoqaUserNmaeBoxXpath,
        demoqaUserName

    )

    # demoqa kullanicisi passwordBox a sifre girer
    sendKey_utils(
        driver,
        demoqaPasswordBoxXpath,
        demoqaPassword
    )

    # demoqa kullanicisi singInButton a tiklar
    click_utils(
        driver,
        demoqaSingInButtonXpath

    )



    time.sleep(2)

    # demoqa kullanicisi dirver kapatir
    driver.quit()
