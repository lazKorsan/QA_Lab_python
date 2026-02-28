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

def navi_loyal_home():
    """Loyal Friend Care ana sayfasına gider."""
    driver.get(loyal_URL)
    time.sleep(2)  # Sayfanın tamamen yüklenmesi için bekleme

def search_progress(searchList):
    """Verilen arama terimi ile arama yapar."""
    sendKey_utils(
        driver,
        loyalfriendSearchBoxXpath,
        searchList,
        "true",
        "true"
    )
    time.sleep(2)  # Arama sonuçlarının yüklenmesi için bekleme

def list_products():
    """Arama sonuçlarını listeler."""
    wrappers = driver.find_elements(By.XPATH, loyalProductList_Xpath)
    product_names = []

    for wrapper in wrappers:
        product_name = wrapper.text  # Ürün adını al
        product_names.append(product_name)

    # Ürün sayısını ve isimlerini yazdır
    print(f"Toplam Ürün Sayısı: {len(product_names)}")
    print("Ürün İsimleri:")
    for name in product_names:
        print(name)

# Kullanici parametreli arama yaptırır
@pytest.mark.parametrize("searchList", ["re", "ra"])
def test_search_time(setup_driver, searchList):
    navi_loyal_home()  # Ana sayfaya git
    search_progress(searchList)  # Arama yap
    list_products()  # Ürünleri listele

if __name__ == "__main__":
    pytest.main()
