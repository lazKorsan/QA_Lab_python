import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.sendkey_utils import sendKey_utils

class LoyalFriendPage:
    """
    LoyalFriend web sitesi için Page Object Model sınıfı.
    """
    loyalUrl = "https://qa.loyalfriendcare.com/en"
    loyalfriendSearchBoxXpath = '//input[@class="form-control"]'
    productNameXpath = '//div[@class="wrapper"]//h3'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate_to_home(self):
        """Ana sayfaya gider."""
        self.driver.get(self.loyalUrl)
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.loyalfriendSearchBoxXpath)))
        print(f"✅ LoyalFriend ana sayfasına gidildi: {self.loyalUrl}")

    def search_product(self, search_term):
        """Arama kutusuna metin girer ve Enter'a basar."""
        print(f"🔍 '{search_term}' aranıyor...")
        sendKey_utils(
            self.driver,
            self.loyalfriendSearchBoxXpath,
            search_term,
            clear_first=True,
            press_enter=True
        )
        # Arama sonuçlarının yüklenmesini bekle
        # Eğer arama sonucu yoksa, bu bekleme başarısız olabilir, bu yüzden try-except kullanabiliriz.
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.productNameXpath)))
            print(f"✅ Arama sonuçları yüklendi.")
        except:
            print(f"⚠️ '{search_term}' için ürün bulunamadı veya arama sonuçları yüklenmedi.")
        time.sleep(1) # Görsel takip için kısa bir bekleme

    def get_product_elements(self):
        """Sayfadaki ürün elementlerini döndürür."""
        return self.driver.find_elements(By.XPATH, self.productNameXpath)

    def get_product_count(self):
        """Bulunan ürün sayısını döndürür."""
        return len(self.get_product_elements())

    def get_product_names(self):
        """Bulunan ürünlerin isimlerini liste olarak döndürür."""
        product_elements = self.get_product_elements()
        return [element.text.strip() for element in product_elements if element.text.strip()]

    def print_product_info(self, search_term):
        """Ürün sayısını ve isimlerini yazdırır."""
        product_count = self.get_product_count()
        product_names = self.get_product_names()

        print(f"\n--- Arama Sonucu: '{search_term}' ---")
        print(f"Toplam Ürün Sayısı: {product_count}")
        if product_count > 0:
            print("Ürün İsimleri:")
            for name in product_names:
                print(f"- {name}")
        else:
            print("Hiç ürün bulunamadı.")
        print("------------------------------------")
