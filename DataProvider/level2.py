import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.sendkey_utils import sendKey_utils

driver = None

loyalfriendSearchBoxXpath = '//input[@class="form-control"]'
loyalUrl = "https://qa.loyalfriendcare.com/en"
productWrapperXpath = '//*[@class="wrapper"]'  # Tüm wrapper elementleri
productNameXpath = './/h4'  # wrapper içindeki ürün ismi (h4 etiketi varsayımı)


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
                # Farklı olasılıkları dene
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

                if product_name:
                    product_names.append({
                        'index': i,
                        'name': product_name
                    })

            except Exception as e:
                print(f"  Ürün {i} ismi alınamadı: {e}")

        return product_names

    except Exception as e:
        print(f"Wrapper elementleri bulunamadı: {e}")
        return []


def test_search_test_loyal():
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(loyalUrl)
    time.sleep(2)

    print("\n" + "=" * 60)
    print("LOYALFRIENDCARE ARAMA TESTİ")
    print("=" * 60)

    # Arama yap
    search_term = "re"
    print(f"\n🔍 Arama terimi: '{search_term}'")

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
        print("\n" + "-" * 40)
        print("ÜRÜN LİSTESİ:")
        print("-" * 40)

        for product in products:
            print(f"{product['index']:2d}. {product['name']}")

        print("-" * 40)

        # İlk ürünün detaylı bilgisi
        if len(products) > 0:
            first_product_xpath = f"({productWrapperXpath})[1]"
            print(f"\n🎯 İlk ürün XPath'i: {first_product_xpath}")
            print(f"   İlk ürün adı: {products[0]['name']}")

    else:
        print("\n❌ Hiç ürün bulunamadı!")

    print("\n" + "=" * 60)

    # Test sonuçlarını dosyaya kaydet (isteğe bağlı)
    save_results_to_file(search_term, products)

    time.sleep(2)
    driver.quit()


def save_results_to_file(search_term, products):
    """Sonuçları bir dosyaya kaydeder"""
    try:
        filename = f"arama_sonuclari_{search_term}_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Arama Terimi: {search_term}\n")
            f.write(f"Tarih: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Bulunan Ürün Sayısı: {len(products)}\n")
            f.write("-" * 40 + "\n")

            for product in products:
                f.write(f"{product['index']}. {product['name']}\n")

        print(f"\n💾 Sonuçlar '{filename}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"Dosya kaydetme hatası: {e}")


if __name__ == "__main__":
    test_search_test_loyal()