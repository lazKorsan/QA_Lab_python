import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.sendkey_utils import sendKey_utils

# Global driver nesnesi
driver = None

loyal_URL = "https://qa.loyalfriendcare.com/en"
loyalfriendSearchBoxXpath = '//input[@class="form-control"]'
loyalProductList_Xpath = '//*[@class="wrapper"]'

@pytest.fixture(scope="module")
def setup_driver():
    global driver
    # Kullanici driver nesnesi olusturur
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    # Her test sonunda kapatılması ve acilmesini saglar
    driver.quit()

# Kullanici parametreli arama yaptırır
@pytest.mark.parametrize("searchList", ["re", "ra"])
def test_search_time(setup_driver, searchList):
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
    wrappers = driver.find_elements(By.XPATH, loyalProductList_Xpath)

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

if __name__ == "__main__":
    pytest.main()

