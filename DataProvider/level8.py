import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

import utils
from utils.search_utils import SearchUtils
from utils.sendkey_utils import sendKey_utils

loyalfriendSearchBoxXpath = '//input[@class="form-control"]'
loyalUrl = "https://qa.loyalfriendcare.com/en"
productWrapperXpath = '//*[@class="wrapper"]'


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.parametrize("search_term", [
    "re",
    "ra"
])
def test_search_loyal_simple(driver, search_term):
    print(f"\n🔍 '{search_term}' aranıyor...")

    driver.get(loyalUrl)
    time.sleep(2)

    sendKey_utils(
        driver,
        loyalfriendSearchBoxXpath,
        search_term,
        "true",
        "true"
    )

    time.sleep(3)

    wrappers = driver.find_elements(By.XPATH, productWrapperXpath)
    product_count = len(wrappers)

    utils = SearchUtils(driver)
    result = utils.search_and_get_results("re")
    utils.print_results(result)
    utils.save_report(result)



