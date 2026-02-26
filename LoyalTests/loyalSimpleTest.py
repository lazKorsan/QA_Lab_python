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

def test_loyal():

    # Kullanici loyalUrl sayfasina gider
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(loyalUrl)
    time.sleep(2)


    # Kullanici login sayfasina gider
    click_utils(
        driver,
        loyalLoginButtonXpath,
        "red"
    )

    # Kullanici login islemlerini gerceklestirir
    # Kullanici mailBox kutusuna gecerli mail bilgisi girer
    sendKey_utils(
        driver,
        loyalMailBoxXpath,
        loyalmail,
    )

    sendKey_utils(
        driver,
        loyalPasswordBoxXpath,
        loyalpassword,
    )

    click_utils(
        driver,
        loyalSubmitButtonXpath,
        "red",
    )

    # Kullanici driver kapatir
    driver.quit()

if __name__ == '__main__':
    test_loyal()








