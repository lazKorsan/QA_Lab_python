import time

from selenium import webdriver

from utils.sendkey_utils import sendKey_utils

driver = None

loyalfriendSearchBoxXpath='//input[@class="form-control"]'
loyalUrl="https://qa.loyalfriendcare.com/en"




def test_search_test_loyal():
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(loyalUrl)
    time.sleep(2)

    sendKey_utils(
        driver,
        loyalfriendSearchBoxXpath,
        "re",
        "true",





    )