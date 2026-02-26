import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.sendkey_utils import sendKey_utils

loyalfriendSearchBoxXpath = '//input[@class="form-control"]'
loyalUrl = "https://qa.loyalfriendcare.com/en"
# productWrapperXpath = '//*[@class="wrapper"]' # Bu XPath'i daha spesifik hale getireceğiz
productNameXpath = '//div[@class="wrapper"]//h3' # Ürün isimlerini doğrudan hedefleyen XPath

@pytest.fixture(scope="module") # scope="module" olarak değiştirildi
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.parametrize("search_term", [
    "re",
    "ra",
    "dog", # Yeni bir arama terimi ekleyelim
    "cat"
])
def test_search_loyal_simple(driver, search_term):
    print(f"\n🔍 '{search_term}' aranıyor...")

    driver.get(loyalUrl)

    # Sayfanın tamamen yüklenmesini bekle
    search_box_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, loyalfriendSearchBoxXpath)))
    
    # Arama kutusuna metin gönder ve Enter'a bas
    sendKey_utils(
        driver,
        loyalfriendSearchBoxXpath,
        search_term,
        clear_first=True, # Önce temizle
        press_enter=True # Enter'a bas
    )

    # Arama sonuçlarının yüklenmesini bekle (örneğin, ürün isimlerinin görünmesini bekle)
    # Eğer arama sonucu yoksa veya sayfa değişmiyorsa, bu bekleme farklı bir elemente göre ayarlanabilir.
    # Şimdilik ürün isimlerinin görünmesini bekleyelim.
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, productNameXpath)))
    except:
        print(f"'{search_term}' için ürün bulunamadı veya sayfa yüklenmedi.")
        # Ürün bulunamazsa testin devam etmesi için boş liste ile devam edebiliriz.
        product_elements = []
    else:
        product_elements = driver.find_elements(By.XPATH, productNameXpath)
    
    product_count = len(product_elements)

    # Ürün sayısını ve isimlerini yazdır
    print(f"Toplam Ürün Sayısı: {product_count}")
    print("Ürün İsimleri:")
    if product_count > 0:
        for product_element in product_elements:
            print(f"- {product_element.text.strip()}")
    else:
        print("Hiç ürün bulunamadı.")
    
    # Her test senaryosu arasında kısa bir bekleme (görsel takip için, otomasyonda genelde önerilmez)
    time.sleep(2)
