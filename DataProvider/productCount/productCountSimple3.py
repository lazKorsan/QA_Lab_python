from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Driver başlat
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    # 1. Siteye git
    driver.get("https://qa.loyalfriendcare.com/en")

    # 2. Search kutusunu bul
    search_box_xpath = '//input[@class="form-control"]'
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, search_box_xpath)))

    # 3. "re" yaz ve ENTER bas
    search_term = "re"
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.ENTER)

    # 4. Arama sonuçlarını bekle
    product_xpath = '//*[@class="wrapper"]'
    wait.until(EC.presence_of_all_elements_located((By.XPATH, product_xpath)))

    products = driver.find_elements(By.XPATH, product_xpath)

    # 5. Toplam ürün sayısını consola yazdır
    total_products = len(products)
    print(f"\nToplam ürün sayısı: {total_products}\n")

    actions = ActionChains(driver)

    product_list = []

    # 6. İnsan hareketini taklit ederek ürünleri gez
    for index, product in enumerate(products, start=1):

        # Scroll ile ürüne git
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", product)
        time.sleep(0.8)

        # Mouse hover
        actions.move_to_element(product).perform()
        time.sleep(0.5)

        # Highlight + üzerine index yaz
        driver.execute_script(f"""
            arguments[0].style.border='3px solid red';
            arguments[0].style.position='relative';

            let label = document.createElement('div');
            label.innerText = 'Ürün {index}';
            label.style.position = 'absolute';
            label.style.top = '0';
            label.style.left = '0';
            label.style.backgroundColor = 'yellow';
            label.style.color = 'black';
            label.style.fontSize = '16px';
            label.style.fontWeight = 'bold';
            label.style.padding = '5px';
            label.style.zIndex = '9999';

            arguments[0].appendChild(label);
        """, product)

        # Ürün adını al (varsa)
        product_text = product.text
        product_list.append(f"{index}. {product_text}")

        print(f"{index}. ürün highlight edildi")
        time.sleep(1)

    # 7. Test sonunda ürün listesini yazdır
    print("\n===== ÜRÜN LİSTESİ =====")
    for item in product_list:
        print(item)

    print(f"\nToplam {total_products} adet ürün bulundu.")

    time.sleep(3)

finally:
    driver.quit()