from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Enter tuşu için gerekli
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 15)
actions = ActionChains(driver)

try:
    # 1. Sayfaya git
    driver.get("https://qa.loyalfriendcare.com/en")

    # 2. Arama kutusuna "re" yaz ve ENTER'a bas
    search_box_xpath = '//input[@class="form-control"]'
    search_input = wait.until(EC.element_to_be_clickable((By.XPATH, search_box_xpath)))

    search_input.clear()  # Varsa eski metni temizle
    search_input.send_keys("re")
    search_input.send_keys(Keys.ENTER)  # <--- ENTER BURADA BASILIYOR

    print("Arama yapıldı, sonuçlar bekleniyor...")

    # Sayfanın yenilenmesi veya sonuçların gelmesi için bekleme
    time.sleep(4)

    # 3. Ürünleri bul
    product_xpath = '//*[@class="wrapper"]'
    # Ürünlerin sayfada belirmesini bekle
    wait.until(EC.presence_of_all_elements_located((By.XPATH, product_xpath)))
    products = driver.find_elements(By.XPATH, product_xpath)

    product_count = len(products)
    product_list_data = []

    print(f"Toplam {product_count} ürün bulundu. İşlem başlıyor...")

    # 4. Döngü ve Görsel Efektler
    for index, product in enumerate(products, start=1):
        # Ürüne odaklan (Scroll)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", product)
        time.sleep(0.8)

        # JS ile Vurgulama ve Sayı Baloncuğu Ekleme
        driver.execute_script("""
            var elem = arguments[0];
            var count = arguments[1];

            // Mevcut stili bozmadan vurgu ekle
            elem.style.outline = '5px solid #FFD700'; // Altın rengi vurgu
            elem.style.position = 'relative';

            var badge = document.createElement('div');
            badge.id = 'automation-badge-' + count;
            badge.innerHTML = count;
            badge.style.position = 'absolute';
            badge.style.top = '10px';
            badge.style.left = '10px';
            badge.style.backgroundColor = 'black';
            badge.style.color = 'yellow';
            badge.style.width = '40px';
            badge.style.height = '40px';
            badge.style.display = 'flex';
            badge.style.alignItems = 'center';
            badge.style.justifyContent = 'center';
            badge.style.borderRadius = '50%';
            badge.style.fontSize = '20px';
            badge.style.fontWeight = 'bold';
            badge.style.zIndex = '9999';
            elem.appendChild(badge);
        """, product, index)

        # Mouse üzerine getir (Hover)
        actions.move_to_element(product).perform()

        # Ürün bilgilerini kaydet
        product_text = product.text.replace('\n', ' ').strip()
        product_list_data.append(product_text)

        time.sleep(1.2)  # İnsan gözüyle takip edilebilir hız

    # 5. Konsol Çıktısı
    print("\n" + "=" * 30)
    print(f"TEST TAMAMLANDI")
    print(f"Bulunan Ürün Sayısı: {product_count}")
    print("=" * 30)
    for i, name in enumerate(product_list_data, 1):
        print(f"{i}. Ürün: {name}")

finally:
    print("\nTarayıcı 5 saniye içinde kapatılacak...")
    time.sleep(5)
    driver.quit()