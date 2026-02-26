import time
import pytest
from selenium import webdriver
from utils.sendkey_utils import sendKey_utils

loyal_URL = "https://qa.loyalfriendcare.com/en"
loyalfriendSearchBoxXpath = '//input[@class="form-control"]'


@pytest.fixture(scope="module")
def driver():
    # WebDriver'ı başlatır
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    # Tüm testler bittikten sonra kapatır
    driver.quit()


@pytest.mark.parametrize("searchList", ["re", "ra"])
def test_search_time(driver, searchList):
    driver.get(loyal_URL)

    # Sayfanın tamamen yüklenmesi için kısa bir bekleme
    time.sleep(2)

    sendKey_utils(
        driver,
        loyalfriendSearchBoxXpath,
        searchList,
        "true",
        "true"
    )
    time.sleep(2)

    # Kullanici arama sonuçlarını listeler

    wrappers = driver.find_elements_by_xpath('//*[@class="wrapper"]')

    



