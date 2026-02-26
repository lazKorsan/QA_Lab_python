import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.sendkey_utils import sendKey_utils

driver = None

loyalfriendSearchBoxXpath = '//input[@class="form-control"]'
loyalUrl = "https://qa.loyalfriendcare.com/en"


def test_search_test_loyal():
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(loyalUrl)
    time.sleep(2)

    # Arama yap
    sendKey_utils(
        driver,
        loyalfriendSearchBoxXpath,
        "re",
        "true",
        "true"
    )

    time.sleep(3)  # Sonuçların yüklenmesi için bekle

    # Tüm wrapper elementlerini bul
    wrappers = driver.find_elements(By.XPATH, '//*[@class="wrapper"]')

    print(f"\n🔍 Bulunan wrapper sayısı: {len(wrappers)}")
    print("\n📦 ÜRÜN LİSTESİ:")
    print("-" * 30)

    # Her wrapper'ın text'ini yazdır
    for i, wrapper in enumerate(wrappers, 1):
        print(f"{i}. {wrapper.text}")
        print("-" * 30)

    time.sleep(2)
    driver.quit()