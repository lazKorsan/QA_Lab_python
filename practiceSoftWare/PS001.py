import time

from selenium import webdriver
from utils.click_utils import click_utils
from utils.sendkey_utils import sendKey_utils
practice_software_loginButton_Xpath='//*[@data-test="nav-sign-in"]'
practice_software_emailBox_Xpath='//input[@id="email"]'
practice_software_passwordBox_Xpath='//input[@id="password"]'
practice_software_loginButton_Xpath2='//input[@data-test="login-submit"]'
practice_software_homePage="https://practicesoftwaretesting.com/"
practice_software_email="lazKorsan123@gmail.com"
practice_software_password = "Query.2026"


def test_practice_software():
    # Kullanici practice software sayfasina gider
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://practicesoftwaretesting.com/")
    time.sleep(2)

    # Kullanici login sayfasina gider
    click_utils(
        driver,
        practice_software_loginButton_Xpath,
        "red"
    )

    # Kullanici login islemlerini gerçekleştirir
    # Kullanici mailBox kutusuna gecerli mail adresi girer
    sendKey_utils(
        driver,
        practice_software_emailBox_Xpath,
        practice_software_email,
        "true",

    )

    # Kullanici passwordBox kutusuna gecerli password girer
    sendKey_utils(
        driver,
        practice_software_passwordBox_Xpath,
        practice_software_password,
        "true",

    )

    # Kullanici login butonuna tiklar
    click_utils(
        driver,
        practice_software_loginButton_Xpath2,
        "purple",
    )








