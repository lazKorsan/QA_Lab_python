import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time


BASE_URL = "https://qa.loyalfriendcare.com/en"
signInButton = '(//*[@class="btn_add"])[1]'


@pytest.mark.parametrize("highlightColour, daireseRenk, click", [
    ("red", "blue", "true"),
    ("green", "purple", "false"),
])
def test_signin_button(highlightColour, daireseRenk, click):

    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(BASE_URL)

        button = wait.until(
            EC.presence_of_element_located((By.XPATH, signInButton))
        )

        # Scroll gerekiyorsa
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        time.sleep(1)

        # Hover gerekiyorsa
        ActionChains(driver).move_to_element(button).perform()
        time.sleep(0.5)

        # Highlight + merkezde dairesel damga
        driver.execute_script(f"""
            arguments[0].style.border='4px solid {highlightColour}';
            arguments[0].style.position='relative';

            let circle = document.createElement('div');
            circle.style.width='40px';
            circle.style.height='40px';
            circle.style.borderRadius='50%';
            circle.style.backgroundColor='{daireseRenk}';
            circle.style.position='absolute';
            circle.style.top='50%';
            circle.style.left='50%';
            circle.style.transform='translate(-50%, -50%)';
            circle.style.opacity='0.6';
            circle.style.zIndex='9999';

            arguments[0].appendChild(circle);
        """, button)

        print("Buton highlight edildi ve merkezine dairesel damga eklendi.")

        # ✅ Görünürlük assert
        is_visible = button.is_displayed()
        assert is_visible, "Buton görünür değil!"
        print("✔ Buton görünür.")

        # ✅ Tıklanabilirlik assert
        is_clickable = wait.until(
            EC.element_to_be_clickable((By.XPATH, signInButton))
        )
        assert is_clickable, "Buton tıklanabilir değil!"
        print("✔ Buton tıklanabilir.")

        click_method_used = "Tıklama yapılmadı"

        # Eğer click true ise basmaya çalış
        if click.lower() == "true":

            print("\nButona basma işlemi başlıyor...")

            # 1️⃣ Normal click
            try:
                button.click()
                click_method_used = "Normal Selenium click()"
            except Exception:

                # 2️⃣ ActionChains click
                try:
                    ActionChains(driver).move_to_element(button).click().perform()
                    click_method_used = "ActionChains click()"
                except Exception:

                    # 3️⃣ JavaScript click
                    try:
                        driver.execute_script("arguments[0].click();", button)
                        click_method_used = "JavaScript click()"
                    except Exception:
                        click_method_used = "Hiçbir yöntemle tıklanamadı"

        print(f"\nTıklama sonucu: {click_method_used}")

        # Buton üzerindeki yazıyı al
        button_text = button.text
        print(f"\nButon üzerindeki yazı: {button_text}")

        time.sleep(2)

    finally:
        driver.quit()