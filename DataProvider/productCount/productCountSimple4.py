import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


BASE_URL = "https://qa.loyalfriendcare.com/en"


@pytest.mark.parametrize("search_term", ["re", "ra", "cat"])
def test_search_and_highlight_products(search_term):

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(BASE_URL)

        search_box_xpath = '//input[@class="form-control"]'
        search_box = wait.until(
            EC.presence_of_element_located((By.XPATH, search_box_xpath))
        )

        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.ENTER)

        time.sleep(2)  # URL değişimi için kısa bekleme

        current_url = driver.current_url
        print(f"\nArama kelimesi: {search_term}")
        print(f"Mevcut URL: {current_url}")

        # ✅ URL değişmedi kontrolü
        if current_url == BASE_URL:
            print("Arama sonucu ürün bulunamadı.\n")
            return

        print("URL değişti, ürünler listeleniyor...\n")

        product_xpath = '//*[@class="wrapper"]'
        wait.until(EC.presence_of_all_elements_located((By.XPATH, product_xpath)))

        products = driver.find_elements(By.XPATH, product_xpath)
        total_products = len(products)

        print(f"Toplam ürün sayısı: {total_products}\n")

        actions = ActionChains(driver)
        product_list = []

        for index, product in enumerate(products, start=1):

            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                product
            )
            time.sleep(0.6)

            actions.move_to_element(product).perform()
            time.sleep(0.4)

            driver.execute_script(f"""
                arguments[0].style.border='3px solid red';
                arguments[0].style.position='relative';

                let label = document.createElement('div');
                label.innerText = 'Ürün {index}';
                label.style.position = 'absolute';
                label.style.top = '0';
                label.style.left = '0';
                label.style.backgroundColor = 'yellow';
                label.style.fontWeight = 'bold';
                label.style.padding = '4px';
                label.style.zIndex = '9999';

                arguments[0].appendChild(label);
            """, product)

            product_list.append(f"{index}. {product.text}")
            print(f"{index}. ürün highlight edildi")
            time.sleep(0.7)

        print("\n===== ÜRÜN LİSTESİ =====")
        for item in product_list:
            print(item)

        print(f"\n{search_term} için toplam {total_products} ürün bulundu.\n")

        time.sleep(2)

    finally:
        driver.quit()