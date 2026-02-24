# click_utils.py
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging
from typing import Union, Optional, List


class ClickUtils:
    """
    Gelişmiş tıklama utilities sınıfı
    Hem Robot Framework hem de Python testlerinde kullanılabilir
    """

    def __init__(self, driver=None, log_level=logging.INFO):
        """
        Args:
            driver: WebDriver instance (Robot Framework'te set edilmeli)
            log_level: Loglama seviyesi
        """
        self.driver = driver
        self.logger = self._setup_logger(log_level)
        self.highlight_color = "yellow"
        self.circle_color = "red"
        self.circle_size = 20

    def _setup_logger(self, log_level):
        """Logger yapılandırması"""
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def set_driver(self, driver):
        """Driver'ı set et (Robot Framework için)"""
        self.driver = driver

    def _draw_circle(self, element, color="red", size=20, duration=1):
        """
        Elementin merkezine daire çizer

        Args:
            element: WebElement
            color: Daire rengi
            size: Daire boyutu (pixel)
            duration: Gösterim süresi
        """
        if not self.driver:
            raise ValueError("Driver set edilmemiş!")

        # Elementin pozisyonunu al
        location = element.location
        size_dict = element.size

        center_x = location['x'] + size_dict['width'] / 2
        center_y = location['y'] + size_dict['height'] / 2

        # Daire çizen JavaScript
        circle_script = f"""
            var circle = document.createElement('div');
            circle.style.position = 'absolute';
            circle.style.left = '{center_x - size / 2}px';
            circle.style.top = '{center_y - size / 2}px';
            circle.style.width = '{size}px';
            circle.style.height = '{size}px';
            circle.style.borderRadius = '50%';
            circle.style.border = '3px solid {color}';
            circle.style.backgroundColor = 'transparent';
            circle.style.zIndex = '9999';
            circle.style.pointerEvents = 'none';
            circle.id = 'click_utils_circle';

            // Eski daireyi temizle
            var oldCircle = document.getElementById('click_utils_circle');
            if (oldCircle) oldCircle.remove();

            document.body.appendChild(circle);

            // Belirtilen süre sonra daireyi kaldır
            setTimeout(function() {{
                var circle = document.getElementById('click_utils_circle');
                if (circle) circle.remove();
            }}, {duration * 1000});
        """

        self.driver.execute_script(circle_script)
        self.logger.info(f"🔴 Daire çizildi - Renk: {color}, Boyut: {size}px")

    def highlight(self, element, color="yellow", duration=1, draw_circle=True, circle_color="red"):
        """
        Elementi vurgula ve isteğe bağlı daire çiz

        Args:
            element: WebElement
            color: Vurgu rengi
            duration: Gösterim süresi
            draw_circle: Daire çizilsin mi?
            circle_color: Daire rengi
        """
        if not self.driver:
            raise ValueError("Driver set edilmemiş!")

        original_style = element.get_attribute('style')

        # Vurgulama
        self.driver.execute_script(
            f"arguments[0].setAttribute('style', arguments[1]);",
            element,
            f"border: 3px solid {color}; background: #ffff99; box-shadow: 0 0 10px {color};"
        )

        # Daire çiz
        if draw_circle:
            self._draw_circle(element, circle_color, self.circle_size, duration)

        time.sleep(duration)

        # Orijinal stili geri yükle
        self.driver.execute_script(
            f"arguments[0].setAttribute('style', arguments[1]);",
            element,
            original_style
        )

    def click(self, xpath: str, color: str = "yellow", timeout: int = 10,
              draw_circle: bool = True, circle_color: str = "red") -> bool:
        """
        İnatçı butonlar için gelişmiş tıklama fonksiyonu

        Args:
            xpath: Butonun XPATH'i
            color: Vurgu rengi
            timeout: Bekleme süresi
            draw_circle: Daire çizilsin mi?
            circle_color: Daire rengi

        Returns:
            bool: Tıklama başarılı mı?
        """
        if not self.driver:
            raise ValueError("Driver set edilmemiş!")

        self.logger.info(f"\n{'=' * 60}")
        self.logger.info(f"🚀 Buton tıklama denemesi başlıyor...")
        self.logger.info(f"    ├─ XPATH: {xpath}")
        self.logger.info(f"    ├─ Renk: {color}")
        self.logger.info(f"    └─ Timeout: {timeout}sn")
        self.logger.info(f"{'=' * 60}")

        try:
            # Elementi bul ve tıklanabilir olana kadar bekle
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

            # Element bilgilerini al
            visible = element.is_displayed()
            enabled = element.is_enabled()
            text = element.text.strip() or element.get_attribute('value') or element.get_attribute(
                'innerText') or 'NoText'
            tag = element.tag_name

            self.logger.info(f"🔍 Buton bilgileri:")
            self.logger.info(f"    ├─ Tag: <{tag}>")
            self.logger.info(f"    ├─ Text: '{text}'")
            self.logger.info(f"    ├─ Görünür: {visible}")
            self.logger.info(f"    └─ Tıklanabilir: {enabled}")

            # Elementi vurgula ve daire çiz
            self.highlight(element, color, 0.5, draw_circle, circle_color)

            # ============= TIKLAMA YÖNTEMLERİ =============

            # YÖNTEM 1: Normal click
            try:
                element.click()
                self.logger.info(f"✅ Yöntem 1 (Normal click) BAŞARILI: '{text}'")
                return True

            except ElementClickInterceptedException:
                self.logger.warning(f"⚠ Yöntem 1 başarısız - Element başka element tarafından engelleniyor")
            except Exception as e:
                self.logger.warning(f"⚠ Yöntem 1 başarısız - {str(e)[:50]}...")

            # YÖNTEM 2: JavaScript click
            try:
                self.driver.execute_script("arguments[0].click();", element)
                self.logger.info(f"✅ Yöntem 2 (JavaScript click) BAŞARILI: '{text}'")
                return True
            except Exception as e:
                self.logger.warning(f"⚠ Yöntem 2 başarısız - {str(e)[:50]}...")

            # YÖNTEM 3: ActionChains
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).click().perform()
                self.logger.info(f"✅ Yöntem 3 (ActionChains) BAŞARILI: '{text}'")
                return True
            except Exception as e:
                self.logger.warning(f"⚠ Yöntem 3 başarısız - {str(e)[:50]}...")

            # YÖNTEM 4: Scroll + click
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                           element)
                time.sleep(0.5)
                element.click()
                self.logger.info(f"✅ Yöntem 4 (Scroll + click) BAŞARILI: '{text}'")
                return True
            except Exception as e:
                self.logger.warning(f"⚠ Yöntem 4 başarısız - {str(e)[:50]}...")

            # YÖNTEM 5: Submit (eğer form elementi ise)
            if tag in ['button', 'input']:
                try:
                    element.submit()
                    self.logger.info(f"✅ Yöntem 5 (Submit) BAŞARILI: '{text}'")
                    return True
                except:
                    pass

            # YÖNTEM 6: Parent click
            try:
                parent = self.driver.execute_script("return arguments[0].parentNode;", element)
                if parent:
                    self.driver.execute_script("arguments[0].click();", parent)
                    self.logger.info(f"✅ Yöntem 6 (Parent click) BAŞARILI: '{text}'")
                    return True
            except:
                pass

            # YÖNTEM 7: disabled kaldır + click
            try:
                self.driver.execute_script("arguments[0].disabled = false;", element)
                time.sleep(0.2)
                element.click()
                self.logger.info(f"✅ Yöntem 7 (Disabled kaldır + click) BAŞARILI: '{text}'")
                return True
            except:
                pass

            # YÖNTEM 8: readonly kaldır + click
            try:
                self.driver.execute_script("arguments[0].removeAttribute('readonly');", element)
                time.sleep(0.2)
                element.click()
                self.logger.info(f"✅ Yöntem 8 (Readonly kaldır + click) BAŞARILI: '{text}'")
                return True
            except:
                pass

            # YÖNTEM 9: Mouse event
            try:
                self.driver.execute_script("""
                    var event = new MouseEvent('click', {
                        view: window,
                        bubbles: true,
                        cancelable: true
                    });
                    arguments[0].dispatchEvent(event);
                """, element)
                self.logger.info(f"✅ Yöntem 9 (Mouse Event) BAŞARILI: '{text}'")
                return True
            except:
                pass

            self.logger.error(f"❌ TÜM YÖNTEMLER BAŞARISIZ! Butona tıklanamadı: '{text}'")
            return False

        except TimeoutException:
            self.logger.error(f"❌ Buton bulunamadı veya tıklanabilir değil: {xpath}")
            return self._try_alternative_xpaths(xpath, color, timeout, draw_circle, circle_color)

        except Exception as e:
            self.logger.error(f"❌ Beklenmeyen hata: {str(e)}")
            return False

    def _try_alternative_xpaths(self, original_xpath: str, color: str, timeout: int,
                                draw_circle: bool, circle_color: str) -> bool:
        """Alternatif XPATH'leri dener"""
        # Alternatif XPATH'leri oluştur
        extracted_text = ""
        if "'" in original_xpath:
            try:
                extracted_text = original_xpath.split("'")[1]
            except IndexError:
                extracted_text = ""

        alt_xpaths = [
            original_xpath,
            f"{original_xpath}[1]",
            f"({original_xpath})[1]",
            original_xpath.replace("button", "div"),
            original_xpath.replace("@type='submit'", "@type='button'"),
            original_xpath.replace("contains(text(),", "contains(@value,"),
            f"//*[contains(text(), '{extracted_text}')]" if extracted_text else original_xpath,
            f"//*[contains(@value, '{extracted_text}')]" if extracted_text else original_xpath,
        ]

        for i, alt_xpath in enumerate(set(alt_xpaths[:5]), 1):  # Benzersiz ilk 5 alternatif
            try:
                self.logger.info(f"🔄 Alternatif {i} deneniyor: {alt_xpath}")
                element = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, alt_xpath))
                )
                self.highlight(element, "orange", 0.5, draw_circle, circle_color)
                element.click()
                self.logger.info(f"✅ Alternatif {i} BAŞARILI!")
                return True
            except:
                continue

        return False

    def click_by_text(self, text: str, tag: str = "button", color: str = "purple",
                      timeout: int = 10, draw_circle: bool = True, circle_color: str = "red") -> bool:
        """Buton metnine göre tıkla"""
        xpath = f"//{tag}[contains(text(), '{text}')]"
        self.logger.info(f"🔍 Metin ile buton aranıyor: '{text}'")
        return self.click(xpath, color, timeout, draw_circle, circle_color)

    def click_by_css(self, css_selector: str, color: str = "blue", timeout: int = 10,
                     draw_circle: bool = True, circle_color: str = "red") -> bool:
        """CSS Selector ile tıkla"""
        self.logger.info(f"🔍 CSS Selector ile buton aranıyor: {css_selector}")

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            )
            self.highlight(element, color, 0.5, draw_circle, circle_color)
            element.click()
            self.logger.info(f"✅ CSS Selector tıklama başarılı!")
            return True
        except:
            return self.click(f"//*[@id='{css_selector}']", color, timeout, draw_circle, circle_color)

    def click_checkbox(self, xpath: Optional[str] = None, element=None, color: str = "green",
                       timeout: int = 10, draw_circle: bool = True, circle_color: str = "blue") -> bool:
        """
        İnatçı checkbox'lar için özel fonksiyon
        """
        self.logger.info(f"\n{'=' * 70}")
        self.logger.info(f"🎯 Checkbox tıklama başlıyor...")
        self.logger.info(f"{'=' * 70}")

        # Element verilmemişse XPATH'den bul
        if element is None and xpath:
            try:
                wait = WebDriverWait(self.driver, timeout)
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            except:
                self.logger.error(f"❌ Checkbox bulunamadı: {xpath}")
                return False

        if not element:
            return False

        # Elementi vurgula ve daire çiz
        self.highlight(element, color, 0.3, draw_circle, circle_color)

        # Element ID'sini al
        element_id = element.get_attribute('id')

        # ============= TÜM TIKLAMA YÖNTEMLERİ =============

        methods = [
            # 1. Direkt checkbox'a tıkla
            lambda: element.click(),

            # 2. JavaScript ile checkbox'a tıkla
            lambda: self.driver.execute_script("arguments[0].click();", element),

            # 3. Label'a tıkla (for attribute)
            lambda: self.driver.find_element(By.XPATH, f"//label[@for='{element_id}']").click(),

            # 4. Parent div'e tıkla
            lambda: self.driver.execute_script("arguments[0].parentNode.click();", element),

            # 5. Parent'ın parent'ına tıkla
            lambda: self.driver.execute_script("arguments[0].parentNode.parentNode.click();", element),

            # 6. Following-sibling
            lambda: self.driver.execute_script("arguments[0].nextSibling.click();", element),

            # 7. Custom-control sınıfına tıkla
            lambda: self.driver.find_element(By.XPATH,
                                             f"//div[contains(@class, 'custom-control') and .//input[@id='{element_id}']]").click(),

            # 8. ActionChains ile tıkla
            lambda: ActionChains(self.driver).move_to_element(element).click().perform(),

            # 9. Space tuşu ile
            lambda: element.send_keys(Keys.SPACE),

            # 10. Enter tuşu ile
            lambda: element.send_keys(Keys.RETURN),

            # 11. Checkbox'ı manuel set et
            lambda: self.driver.execute_script("""
                arguments[0].checked = true; 
                arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                arguments[0].dispatchEvent(new Event('click', {bubbles: true}));
            """, element),

            # 12. CSS ile background'a tıkla
            lambda: self.driver.execute_script("""
                var checkbox = arguments[0];
                var rect = checkbox.getBoundingClientRect();
                var event = new MouseEvent('click', {
                    view: window,
                    bubbles: true,
                    cancelable: true,
                    clientX: rect.left + rect.width/2,
                    clientY: rect.top + rect.height/2
                });
                checkbox.dispatchEvent(event);
            """, element),
        ]

        # Tüm metodları dene
        for i, method in enumerate(methods, 1):
            try:
                method()
                time.sleep(0.2)

                # Checkbox seçildi mi kontrol et
                is_checked = self.driver.execute_script("return arguments[0].checked;", element)

                if is_checked:
                    self.logger.info(f"✅ Yöntem {i} BAŞARILI! Checkbox seçildi.")
                    self.highlight(element, "green", 0.5, draw_circle, "green")
                    return True
                else:
                    self.logger.warning(f"⚠ Yöntem {i} çalıştı ama checkbox seçilmedi?")

            except Exception as e:
                self.logger.warning(f"⚠ Yöntem {i} başarısız: {str(e)[:30]}...")
                continue

        # SON ÇARE: Tüm checkbox'ları dene
        return self._try_all_checkboxes(draw_circle, circle_color)

    def _try_all_checkboxes(self, draw_circle: bool, circle_color: str) -> bool:
        """Son çare olarak tüm checkbox'ları dener"""
        try:
            self.logger.info(f"🔄 SON ÇARE: Tüm checkbox'lar taranıyor...")
            all_checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")

            for idx, cb in enumerate(all_checkboxes):
                try:
                    self.driver.execute_script("""
                        arguments[0].checked = true; 
                        arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                    """, cb)

                    if draw_circle:
                        self._draw_circle(cb, circle_color, self.circle_size, 0.5)

                    self.logger.info(f"✅ Son çare - Checkbox {idx + 1} seçildi!")
                    return True
                except:
                    continue
        except:
            pass

        self.logger.error(f"❌ TÜM YÖNTEMLER BAŞARISIZ!")
        return False

    def click_terms_checkbox(self, timeout: int = 10, draw_circle: bool = True,
                             circle_color: str = "blue") -> bool:
        """Özel olarak terms&conditions checkbox'ını tıkla"""

        xpaths = [
            "//input[@type='checkbox' and @id='term']",
            "//input[@type='checkbox' and @name='term']",
            "//label[@for='term']",
            "//div[contains(@class, 'custom-checkbox')]",
            "//span[contains(@class, 'custom-control')]",
            "//label[contains(text(), 'I agree')]",
            "//label[contains(text(), 'terms')]/..",
            "//label[contains(text(), 'kabul ediyorum')]/..",
            "//label[contains(text(), 'onaylıyorum')]/..",
            "(//input[@type='checkbox'])[1]",
            "(//input[@type='checkbox'])[last()]",
            "//input[@type='checkbox'][1]",
        ]

        for xpath in xpaths:
            try:
                element = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )

                # Eğer element label veya div ise, içindeki checkbox'ı bul
                if element.tag_name in ['label', 'div', 'span']:
                    checkbox = element.find_elements(By.XPATH, ".//input[@type='checkbox']")
                    if checkbox:
                        return self.click_checkbox(element=checkbox[0], draw_circle=draw_circle,
                                                   circle_color=circle_color)

                # Direkt tıkla
                return self.click_checkbox(element=element, draw_circle=draw_circle,
                                           circle_color=circle_color)

            except:
                continue

        return False

    def set_circle_properties(self, color: str = "red", size: int = 20):
        """Daire özelliklerini ayarla"""
        self.circle_color = color
        self.circle_size = size
        self.logger.info(f"⚙ Daire özellikleri ayarlandı - Renk: {color}, Boyut: {size}px")


# ==================== ROBOT FRAMEWORK KEYWORD'LERİ ====================
# Robot Framework için ayrı bir sınıf

class RobotClickUtils:
    """Robot Framework için ClickUtils keywordleri"""

    def __init__(self):
        self.click_utils = ClickUtils()

    def set_driver(self, driver):
        """Driver'ı set et"""
        self.click_utils.set_driver(driver)

    def click_element(self, xpath, color="yellow", timeout=10, draw_circle=True, circle_color="red"):
        """Elemente tıkla (Robot Framework keyword)"""
        return self.click_utils.click(xpath, color, int(timeout),
                                      self._str_to_bool(draw_circle), circle_color)

    def click_element_by_text(self, text, tag="button", color="purple", timeout=10,
                              draw_circle=True, circle_color="red"):
        """Metne göre elemente tıkla"""
        return self.click_utils.click_by_text(text, tag, color, int(timeout),
                                              self._str_to_bool(draw_circle), circle_color)

    def click_checkbox(self, xpath=None, color="green", timeout=10, draw_circle=True, circle_color="blue"):
        """Checkbox'a tıkla"""
        return self.click_utils.click_checkbox(xpath=xpath, color=color, timeout=int(timeout),
                                               draw_circle=self._str_to_bool(draw_circle),
                                               circle_color=circle_color)

    def click_terms_checkbox_keyword(self, timeout=10, draw_circle=True, circle_color="blue"):
        """Terms checkbox'ına tıkla"""
        return self.click_utils.click_terms_checkbox(timeout=int(timeout),
                                                     draw_circle=self._str_to_bool(draw_circle),
                                                     circle_color=circle_color)

    def set_circle_options(self, color="red", size=20):
        """Daire seçeneklerini ayarla"""
        self.click_utils.set_circle_properties(color, int(size))

    def _str_to_bool(self, value):
        """String değeri boolean'a çevir (Robot Framework için)"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ['true', 'yes', '1', 'on']
        return bool(value)


# ==================== GERİYE UYUMLULUK İÇİN FONKSİYONLAR ====================
# Eski kodları kırmamak için fonksiyonları da koruyoruz

_click_utils_instance = None


def _get_instance(driver=None):
    """Singleton instance oluştur veya mevcut instance'ı kullan"""
    global _click_utils_instance
    if _click_utils_instance is None:
        _click_utils_instance = ClickUtils(driver)
    elif driver and _click_utils_instance.driver is None:
        _click_utils_instance.set_driver(driver)
    return _click_utils_instance


def highlight(driver, element, color="yellow", duration=1):
    """Geriye uyumluluk için highlight fonksiyonu"""
    utils = _get_instance(driver)
    utils.highlight(element, color, duration, draw_circle=False)


def click_utils(driver, xpath, color="yellow", timeout=10):
    """Geriye uyumluluk için click_utils fonksiyonu"""
    utils = _get_instance(driver)
    return utils.click(xpath, color, timeout, draw_circle=False)


def click_utils_by_text(driver, text, tag="button", color="purple", timeout=10):
    """Geriye uyumluluk için click_utils_by_text fonksiyonu"""
    utils = _get_instance(driver)
    return utils.click_by_text(text, tag, color, timeout, draw_circle=False)


def click_utils_by_css(driver, css_selector, color="blue", timeout=10):
    """Geriye uyumluluk için click_utils_by_css fonksiyonu"""
    utils = _get_instance(driver)
    return utils.click_by_css(css_selector, color, timeout, draw_circle=False)


def click_checkbox_utils(driver, xpath=None, element=None, color="green", timeout=10):
    """Geriye uyumluluk için click_checkbox_utils fonksiyonu"""
    utils = _get_instance(driver)
    return utils.click_checkbox(xpath, element, color, timeout, draw_circle=False)


def click_terms_checkbox(driver, timeout=10):
    """Geriye uyumluluk için click_terms_checkbox fonksiyonu"""
    utils = _get_instance(driver)
    return utils.click_terms_checkbox(timeout, draw_circle=False)