import time


from selenium import webdriver
from utils.click_utils import click_utils
from utils.sendkey_utils import sendKey_utils

driver = None

geekUrl="https://www.geeksforgeeks.org/"
geekLoginButtonXpath='//button[@class="signinButton gfg_loginModalBtn login-modal-btn"]'
geekMailBoxXpath='//input[@placeholder="Username or Email"]'
geekPasswordBoxXpath='//input[@placeholder="Enter password"]'
geekLoginPageSubmitButtonXpath='//button[@class="loginBtn btnGreen notSocialAuthBtn"]'
geekMail="jemote1577@pazuric.com"
password="Query.2026!"





def test_geek():

    # Kullanici geekHomePage sayfasina gider
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(geekUrl)
    time.sleep(2)


    # Kullanici geekLoginPage sayfasina gider

    click_utils(
        driver,
        geekLoginButtonXpath,
        "red"
    )


    # Kullanici login islemlerini gerceklestirir
    # Kullanici mailBox kutusuna gecerli mail bilgisi girer
    sendKey_utils(
        driver,
        geekMailBoxXpath,
        geekMail,

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

    # Kullanici driver kapatir
    driver.quit()

if __name__ == '__main__':
    test_geek()





