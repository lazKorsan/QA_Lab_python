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

    # Ürün isimlerini ve sayısını toplamak için bir liste
    product_names = []

    for wrapper in wrappers:
        # Her bir wrapper içindeki ürün adını bul
        product_name = wrapper.text  # veya uygun bir xpath ile ürün adını alabilirsiniz
        product_names.append(product_name)

    # Ürün sayısını ve isimlerini yazdır
    print(f"Toplam Ürün Sayısı: {len(product_names)}")
    print("Ürün İsimleri:")
    for name in product_names:
        print(name)

