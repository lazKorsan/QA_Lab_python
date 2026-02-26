import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.sendkey_utils import sendKey_utils

# Test verileri - Data provider gibi
test_data = [
    ("re", "re ile arama sonuçları"),
    ("ra", "ra ile arama sonuçları")
]

loyalfriendSearchBoxXpath = '//input[@class="form-control"]'
loyalUrl = "https://qa.loyalfriendcare.com/en"
productWrapperXpath = '//*[@class="wrapper"]'


@pytest.fixture(scope="function")
def driver():
    """Her test için yeni driver oluştur"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def get_product_names(driver):
    """Arama sonuçlarındaki ürün isimlerini toplar"""
    try:
        # Tüm wrapper elementlerini bul
        wrappers = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, productWrapperXpath))
        )

        product_names = []

        # Her wrapper içinde ürün ismini ara
        for i, wrapper in enumerate(wrappers, 1):
            try:
                # Ürün ismini bul (h4, h3 veya product-title class'ı olabilir)
                product_name = None

                # 1. h4 etiketi dene
                try:
                    name_element = wrapper.find_element(By.XPATH, './/h4')
                    product_name = name_element.text
                except:
                    pass

                # 2. h3 etiketi dene
                if not product_name:
                    try:
                        name_element = wrapper.find_element(By.XPATH, './/h3')
                        product_name = name_element.text
                    except:
                        pass

                # 3. product-title class'ı dene
                if not product_name:
                    try:
                        name_element = wrapper.find_element(By.XPATH, './/*[contains(@class, "title")]')
                        product_name = name_element.text
                    except:
                        pass

                # 4. Hiçbiri yoksa wrapper'ın kendi text'ini al
                if not product_name:
                    product_name = wrapper.text.strip()

                if product_name and product_name.strip():
                    product_names.append({
                        'index': i,
                        'name': product_name.strip()
                    })

            except Exception as e:
                print(f"  Ürün {i} ismi alınamadı: {e}")

        return product_names

    except Exception as e:
        print(f"Wrapper elementleri bulunamadı: {e}")
        return []


def save_results_to_file(search_term, products):
    """Sonuçları bir dosyaya kaydeder"""
    try:
        filename = f"arama_sonuclari_{search_term}_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Arama Terimi: {search_term}\n")
            f.write(f"Tarih: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Bulunan Ürün Sayısı: {len(products)}\n")
            f.write("-" * 40 + "\n")
            f.write("ÜRÜN LİSTESİ:\n")
            f.write("-" * 40 + "\n")

            for product in products:
                f.write(f"{product['index']:2d}. {product['name']}\n")

        print(f"\n💾 Sonuçlar '{filename}' dosyasına kaydedildi.")
        return filename
    except Exception as e:
        print(f"Dosya kaydetme hatası: {e}")
        return None


@pytest.mark.parametrize("search_term, description", test_data)
def test_search_loyal(driver, search_term, description):
    """Data provider ile çalışan arama testi"""

    print("\n" + "=" * 70)
    print(f"🔍 TEST BAŞLADI: {description}")
    print(f"📝 Arama terimi: '{search_term}'")
    print("=" * 70)

    # Siteyi aç
    driver.get(loyalUrl)
    time.sleep(2)

    # Arama yap
    sendKey_utils(
        driver,
        loyalfriendSearchBoxXpath,
        search_term,
        "true",
        "true"
    )

    # Arama sonuçlarının yüklenmesi için bekle
    time.sleep(3)

    # Ürün isimlerini al
    products = get_product_names(driver)

    # Sonuçları listele
    if products:
        print(f"\n📦 Bulunan ürün sayısı: {len(products)}")
        print("\n" + "-" * 50)
        print("ÜRÜN LİSTESİ:")
        print("-" * 50)

        for product in products[:10]:  # İlk 10 ürünü göster (çok varsa)
            print(f"{product['index']:2d}. {product['name'][:50]}...")  # Uzun isimleri kısalt

        if len(products) > 10:
            print(f"   ... ve {len(products) - 10} ürün daha")

        print("-" * 50)

        # İlk ürünün detaylı bilgisi
        if len(products) > 0:
            print(f"\n🎯 İlk ürün: {products[0]['name']}")

        # Sonuçları dosyaya kaydet
        saved_file = save_results_to_file(search_term, products)

        # Test assertion - en az 1 ürün bulunmalı
        assert len(products) > 0, f"'{search_term}' aramasında hiç ürün bulunamadı!"

    else:
        print(f"\n❌ '{search_term}' aramasında hiç ürün bulunamadı!")
        assert False, f"'{search_term}' aramasında hiç ürün bulunamadı!"

    print("\n" + "=" * 70)
    print(f"✅ TEST TAMAMLANDI: {description}")
    print("=" * 70 + "\n")


# Alternatif: Farklı data provider formatı
@pytest.mark.parametrize("search_term", [
    "re",
    "ra",
    "do",  # Ek testler ekleyebilirsiniz
    "ca",
    "ma"
])
def test_search_loyal_simple(driver, search_term):
    """Basit data provider ile arama testi"""

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

    print(f"📦 '{search_term}' için {product_count} ürün bulundu")

    # İlk 3 ürünü göster
    for i, wrapper in enumerate(wrappers[:3], 1):
        print(f"   {i}. {wrapper.text[:30]}...")

    # En az 1 ürün bulunmalı
    assert product_count > 0, f"'{search_term}' aramasında ürün bulunamadı!"

    time.sleep(1)


# Eğer pytest'i doğrudan çalıştırmak isterseniz:
if __name__ == "__main__":
    # Tek test için manuel çalıştırma
    test_driver = webdriver.Chrome()
    test_driver.maximize_window()

    # Tüm test verilerini manuel çalıştır
    for search_term, description in test_data:
        print("\n" + "=" * 70)
        print(f"MANUEL TEST: {description}")

        test_driver.get(loyalUrl)
        time.sleep(2)

        sendKey_utils(
            test_driver,
            loyalfriendSearchBoxXpath,
            search_term,
            "true",
            "true"
        )

        time.sleep(3)

        wrappers = test_driver.find_elements(By.XPATH, productWrapperXpath)
        print(f"📦 '{search_term}' için {len(wrappers)} ürün bulundu")

        time.sleep(1)

    test_driver.quit()