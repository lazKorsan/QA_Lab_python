import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    # Sayfanın tamamen yüklenmesini bekle
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, loyalfriendSearchBoxXpath)))

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
    result = utils.search_and_get_results(search_term)
    utils.print_results(result)
    utils.save_report(result)

    # Ürün sayısını ve isimlerini yazdır
    print(f"Toplam Ürün Sayısı: {product_count}")
    print("Ürün İsimleri:")
    for wrapper in wrappers:
        print(wrapper.text)
