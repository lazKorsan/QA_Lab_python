from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Ayarlar
searchList = ["re", "ra", "cat"]
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)
actions = ActionChains(driver)

# Genel bir rapor tutmak istersen diye sözlük yapısı
final_report = {}

try:
    for searchTerm in searchList:
        print(f"\n{'=' * 50}")
        print(f">>> ARAMA BAŞLATILIYOR: '{searchTerm}'")
        print(f"{'=' * 50}")

        driver.get("https://qa.loyalfriendcare.com/en")

        search_box_xpath = '//input[@class="form-control"]'
        search_input = wait.until(EC.element_to_be_clickable((By.XPATH, search_box_xpath)))

        search_input.clear()
        search_input.send_keys(searchTerm)
        search_input.send_keys(Keys.ENTER)

        time.sleep(3)  # Sonuçların gelmesini bekle

        product_xpath = '//*[@class="wrapper"]'
        products = driver.find_elements(By.XPATH, product_xpath)

        product_count = len(products)
        current_search_products = []  # Bu arama için isimleri tutacak liste

        # Ürünleri Gez ve Veri Topla
        for index, product in enumerate(products, start=1):
            # Sayfayı kaydır
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", product)
            time.sleep(0.4)

            # Ürün ismini al (İlk satırı temizle ve al)
            product_name = product.text.split('\n')[0].strip()
            current_search_products.append(product_name)

            # Görsel Vurgu ve Numara (JS)
            driver.execute_script("""
                var elem = arguments[0];
                var count = arguments[1];
                var term = arguments[2];

                elem.style.border = '4px solid #FF5733'; // Turuncu/Kırmızı vurgu
                elem.style.position = 'relative';

                var badge = document.createElement('div');
                badge.innerHTML = term + " #" + count;
                badge.style.position = 'absolute';
                badge.style.top = '0';
                badge.style.left = '0';
                badge.style.backgroundColor = '#FF5733';
                badge.style.color = 'white';
                badge.style.padding = '4px 8px';
                badge.style.fontSize = '12px';
                badge.style.fontWeight = 'bold';
                badge.style.zIndex = '1000';
                elem.appendChild(badge);
            """, product, index, searchTerm)

            actions.move_to_element(product).perform()
            time.sleep(0.6)

        # Aramayı genel rapora kaydet
        final_report[searchTerm] = current_search_products

        # --- ANLIK KONSOL ÇIKTISI ---
        print(f"\n[SONUÇ] '{searchTerm}' için toplam {product_count} ürün listeleniyor:")
        if product_count > 0:
            for i, name in enumerate(current_search_products, 1):
                print(f"  {i}. {name}")
        else:
            print("  (!) Hiç ürün bulunamadı.")

        time.sleep(2)

    # --- FİNAL ÖZET RAPORU ---
    print(f"\n\n{'*' * 20} GENEL TEST ÖZETİ {'*' * 20}")
    for term, items in final_report.items():
        print(f"- '{term}': {len(items)} Ürün bulundu.")
    print(f"{'*' * 58}")

except Exception as e:
    print(f"Hata oluştu: {e}")

finally:
    print("\nTest bitti, tarayıcı 5 saniye içinde kapatılacak.")
    time.sleep(5)
    driver.quit()