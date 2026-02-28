"""
Search Utilities - Gelişmiş Arama ve Ürün Çekme Sınıfı
Author: QA Engineer
Date: 2024
"""

import time
import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any, Union
from dataclasses import dataclass, field, asdict
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException


@dataclass
class ProductDetail:
    """Ürün detay veri sınıfı"""
    name: str = ""
    price: str = ""
    link: str = ""
    image: str = ""
    sku: str = ""
    brand: str = ""
    description: str = ""
    specifications: Dict[str, str] = field(default_factory=dict)
    all_text: str = ""

    def to_dict(self) -> Dict:
        """Sözlük formatına çevirir"""
        return asdict(self)

    def summary(self) -> str:
        """Özet bilgi döndürür"""
        return f"{self.name} - {self.price}"


@dataclass
class SearchResult:
    """Arama sonucu veri sınıfı"""
    term: str
    product_count: int
    products: List[ProductDetail]
    search_time: float
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def summary(self) -> str:
        """Sonuç özeti döndürür"""
        return f"'{self.term}' için {self.product_count} ürün ({self.search_time:.2f}s)"


class ProductExtractor:
    """
    Ürün detaylarını çıkaran gelişmiş sınıf
    Her türlü HTML yapısından ürün bilgilerini çıkarabilir
    """

    def __init__(self, driver: WebDriver, timeout: int = 5):
        self.driver = driver
        self.timeout = timeout

    def extract_from_element(self,
                            element: WebElement,
                            locator_config: Optional[Dict] = None) -> ProductDetail:
        """
        Bir WebElement'ten ürün detaylarını çıkarır

        Args:
            element: Ürün elementi
            locator_config: Özel locator konfigürasyonu

        Returns:
            ProductDetail objesi
        """
        product = ProductDetail()

        try:
            # Tüm text'i al
            product.all_text = element.text.strip()

            # Varsayılan locator'lar
            default_locators = {
                'name': [
                    './/h1', './/h2', './/h3', './/h4',
                    './/*[contains(@class, "title")]',
                    './/*[contains(@class, "name")]',
                    './/*[contains(@class, "product-name")]',
                    './/*[@itemprop="name"]'
                ],
                'price': [
                    './/*[contains(@class, "price")]',
                    './/*[contains(@class, "fiyat")]',
                    './/*[contains(@class, "sale-price")]',
                    './/*[contains(@class, "current-price")]',
                    './/*[@itemprop="price"]',
                    './/ins', './/span[contains(@class, "price")]'
                ],
                'link': [
                    './/a/@href',
                    './/a'
                ],
                'image': [
                    './/img/@src',
                    './/img/@data-src',
                    './/img'
                ],
                'sku': [
                    './/*[contains(@class, "sku")]',
                    './/*[contains(@class, "code")]',
                    './/*[@itemprop="sku"]'
                ],
                'brand': [
                    './/*[contains(@class, "brand")]',
                    './/*[contains(@class, "marka")]',
                    './/*[@itemprop="brand"]'
                ],
                'description': [
                    './/*[contains(@class, "description")]',
                    './/*[contains(@class, "aciklama")]',
                    './/*[@itemprop="description"]'
                ]
            }

            # Özel locator varsa onu kullan, yoksa varsayılanı
            locators = locator_config if locator_config else default_locators

            # Her bir alanı dene
            for field, xpath_list in locators.items():
                if field == 'all_text':
                    continue

                value = self._extract_field(element, field, xpath_list)
                if value:
                    setattr(product, field, value)

            # Spesifikasyonları çıkar (tablo yapısı varsa)
            product.specifications = self._extract_specifications(element)

        except Exception as e:
            print(f"⚠️ Ürün çıkarılırken hata: {e}")

        return product

    def _extract_field(self, element: WebElement, field_name: str, xpath_list: List[str]) -> Optional[str]:
        """Tek bir alanı çıkarmayı dener"""
        for xpath in xpath_list:
            try:
                if xpath.endswith('/@href') or xpath.endswith('/@src'):
                    # Attribute çekme
                    real_xpath = xpath.replace('/@href', '').replace('/@src', '')
                    attr_name = 'href' if '/@href' in xpath else 'src'
                    sub_element = element.find_element(By.XPATH, real_xpath)
                    value = sub_element.get_attribute(attr_name)
                    if value:
                        return value
                else:
                    # Element text'i çekme
                    sub_element = element.find_element(By.XPATH, xpath)
                    value = sub_element.text.strip()
                    if value:
                        return value
            except:
                continue
        return None

    def _extract_specifications(self, element: WebElement) -> Dict[str, str]:
        """Ürün spesifikasyonlarını çıkarır (tablo formatında)"""
        specs = {}
        try:
            # Tablo satırlarını bul
            rows = element.find_elements(By.XPATH, './/tr')
            for row in rows:
                try:
                    cells = row.find_elements(By.XPATH, './/td | .//th')
                    if len(cells) >= 2:
                        key = cells[0].text.strip()
                        value = cells[1].text.strip()
                        if key and value:
                            specs[key] = value
                except:
                    continue

            # Alternatif: div-based specs
            if not specs:
                spec_items = element.find_elements(By.XPATH, './/*[contains(@class, "spec")]')
                for item in spec_items:
                    text = item.text.strip()
                    if ':' in text:
                        key, value = text.split(':', 1)
                        specs[key.strip()] = value.strip()

        except Exception as e:
            print(f"⚠️ Spesifikasyon çıkarılamadı: {e}")

        return specs


class AdvancedSearchUtils:
    """
    Gelişmiş Arama ve Ürün Çekme Sınıfı
    Esnek ve her site için kullanılabilir
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        AdvancedSearchUtils sınıfı başlatıcı

        Args:
            driver: Selenium WebDriver instance
            timeout: Varsayılan bekleme süresi
        """
        self.driver = driver
        self.timeout = timeout
        self.search_history: List[SearchResult] = []
        self.extractor = ProductExtractor(driver, timeout)
        self.report_dir = self._create_report_directory()

    def _create_report_directory(self) -> Path:
        """Raporlar için dizin oluşturur"""
        report_dir = Path.cwd() / "test_reports" / "product_data"
        report_dir.mkdir(parents=True, exist_ok=True)
        return report_dir

    def _wait_for_element(self, by: By, value: str, timeout: Optional[int] = None) -> Optional[WebElement]:
        """Elementin görünmesini bekler"""
        try:
            wait_time = timeout or self.timeout
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"⚠️ Element bulunamadı: {value}")
            return None

    def search_and_get_products(self,
                               search_term: str,
                               search_box_locator: Union[str, Tuple[By, str]],
                               product_list_locator: Union[str, Tuple[By, str]],
                               wait_after_search: int = 3,
                               clear_before_search: bool = True,
                               max_products: int = 50,
                               load_more_button_locator: Optional[Union[str, Tuple[By, str]]] = None,
                               custom_extractor_config: Optional[Dict] = None) -> SearchResult:
        """
        Arama yapar ve ürün listesini döndürür

        Args:
            search_term: Aranacak kelime
            search_box_locator: Arama kutusu locator'ı (string XPath veya (By, value) tuple)
            product_list_locator: Ürün listesi locator'ı
            wait_after_search: Arama sonrası bekleme süresi
            clear_before_search: Aramadan önce kutuyu temizle
            max_products: Çekilecek maksimum ürün sayısı
            load_more_button_locator: "Daha fazla" butonu locator'ı
            custom_extractor_config: Özel extractor konfigürasyonu

        Returns:
            SearchResult objesi
        """
        start_time = time.time()

        # Locator'ları standardize et
        search_by, search_value = self._parse_locator(search_box_locator)
        product_by, product_value = self._parse_locator(product_list_locator)

        products = []

        try:
            # Arama kutusunu bul
            search_box = self._wait_for_element(search_by, search_value)
            if not search_box:
                raise Exception(f"Arama kutusu bulunamadı")

            if clear_before_search:
                search_box.clear()

            # Arama yap
            search_box.send_keys(search_term)
            search_box.submit()

            # Sonuçların yüklenmesini bekle
            time.sleep(wait_after_search)

            # Ürünleri bul
            product_elements = self.driver.find_elements(product_by, product_value)

            # "Daha fazla" butonu varsa tıkla ve ürünleri yükle
            if load_more_button_locator:
                load_by, load_value = self._parse_locator(load_more_button_locator)
                self._load_all_products(load_by, load_value, product_by, product_value, max_products)

            # Ürünleri çek
            for i, element in enumerate(product_elements[:max_products], 1):
                print(f"  📦 Ürün {i}/{min(len(product_elements), max_products)} çekiliyor...")

                product_detail = self.extractor.extract_from_element(
                    element,
                    custom_extractor_config
                )

                # Eğer isim boşsa ve element text'i varsa onu kullan
                if not product_detail.name and element.text.strip():
                    product_detail.name = element.text.strip()[:100]

                products.append(product_detail)

        except Exception as e:
            print(f"❌ Arama sırasında hata: {e}")

        # Arama sonucu oluştur
        search_time = time.time() - start_time
        result = SearchResult(
            term=search_term,
            product_count=len(products),
            products=products,
            search_time=search_time
        )

        self.search_history.append(result)
        return result

    def get_product_details(self,
                           product_locator: Union[str, Tuple[By, str]],
                           wait_for_details: bool = True,
                           extractor_config: Optional[Dict] = None) -> ProductDetail:
        """
        Tek bir ürünün detaylarını çeker

        Args:
            product_locator: Ürün elementi locator'ı
            wait_for_details: Detayların yüklenmesini bekle
            extractor_config: Özel extractor konfigürasyonu

        Returns:
            ProductDetail objesi
        """
        by, value = self._parse_locator(product_locator)

        # Ürün elementini bul
        product_element = self._wait_for_element(by, value, timeout=self.timeout)
        if not product_element:
            raise Exception(f"Ürün bulunamadı: {value}")

        # Detayların yüklenmesini bekle (opsiyonel)
        if wait_for_details:
            time.sleep(2)

        # Ürün detaylarını çıkar
        product_detail = self.extractor.extract_from_element(product_element, extractor_config)

        return product_detail

    def _parse_locator(self, locator: Union[str, Tuple[By, str]]) -> Tuple[By, str]:
        """
        Locator'ı (By, value) formatına çevirir

        Args:
            locator: String XPath veya (By, value) tuple

        Returns:
            (By, value) tuple
        """
        if isinstance(locator, tuple):
            return locator
        else:
            return (By.XPATH, locator)

    def _load_all_products(self,
                          load_by: By,
                          load_value: str,
                          product_by: By,
                          product_value: str,
                          max_products: int):
        """
        Tüm ürünleri yüklemek için "daha fazla" butonuna tıklar
        """
        try:
            max_clicks = 20  # Maksimum tıklama sayısı
            click_count = 0

            while click_count < max_clicks:
                try:
                    # Mevcut ürün sayısı
                    current_count = len(self.driver.find_elements(product_by, product_value))

                    if current_count >= max_products:
                        break

                    # "Daha fazla" butonunu bul ve tıkla
                    load_button = self.driver.find_element(load_by, load_value)

                    if load_button.is_enabled():
                        load_button.click()
                        time.sleep(2)  # Yeni ürünlerin yüklenmesini bekle
                        click_count += 1

                        # Yeni ürün sayısı
                        new_count = len(self.driver.find_elements(product_by, product_value))

                        if new_count <= current_count:  # Ürün artmıyorsa dur
                            break
                    else:
                        break

                except:
                    break

        except Exception as e:
            print(f"⚠️ Ürün yükleme sırasında hata: {e}")

    def print_product_details(self, product: ProductDetail, detailed: bool = False):
        """
        Ürün detaylarını yazdırır

        Args:
            product: ProductDetail objesi
            detailed: Tüm detayları göster
        """
        print("\n" + "=" * 70)
        print("📦 ÜRÜN DETAYI")
        print("=" * 70)

        print(f"📝 İsim: {product.name}")
        print(f"💰 Fiyat: {product.price or 'Bulunamadı'}")
        print(f"🔗 Link: {product.link or 'Bulunamadı'}")
        print(f"🖼️  Resim: {product.image or 'Bulunamadı'}")
        print(f"🏷️  SKU: {product.sku or 'Bulunamadı'}")
        print(f"🏭 Marka: {product.brand or 'Bulunamadı'}")

        if product.description:
            print(f"📄 Açıklama: {product.description[:200]}...")

        if detailed and product.specifications:
            print("\n📋 ÖZELLİKLER:")
            for key, value in list(product.specifications.items())[:10]:
                print(f"   • {key}: {value}")

        if detailed and product.all_text:
            print(f"\n📜 TÜM METİN (ilk 500 karakter):")
            print(f"   {product.all_text[:500]}...")

        print("=" * 70)

    def save_products_to_json(self,
                              result: SearchResult,
                              filename: Optional[str] = None) -> Path:
        """
        Ürünleri JSON formatında kaydeder

        Args:
            result: SearchResult objesi
            filename: Özel dosya adı

        Returns:
            Kaydedilen dosya yolu
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"products_{result.term}_{timestamp}.json"

        file_path = self.report_dir / filename

        # JSON için hazırla
        data = {
            "search_term": result.term,
            "timestamp": result.timestamp,
            "search_time": result.search_time,
            "total_products": result.product_count,
            "products": [p.to_dict() for p in result.products]
        }

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"💾 JSON kaydedildi: {file_path}")
            return file_path

        except Exception as e:
            print(f"❌ JSON kaydedilemedi: {e}")
            return file_path

    def compare_products(self, product1: ProductDetail, product2: ProductDetail) -> Dict:
        """
        İki ürünü karşılaştırır

        Returns:
            Karşılaştırma sonuçları
        """
        comparison = {
            "name_match": product1.name == product2.name,
            "price_match": product1.price == product2.price,
            "brand_match": product1.brand == product2.brand,
            "sku_match": product1.sku == product2.sku,
            "details": {
                "product1": product1.summary(),
                "product2": product2.summary()
            }
        }

        return comparison


# KOLAY KULLANIM İÇİN YARDIMCI FONKSİYONLAR

def search_products(driver: WebDriver,
                   search_term: str,
                   search_box: Union[str, Tuple[By, str]],
                   product_list: Union[str, Tuple[By, str]]) -> SearchResult:
    """
    Basit arama fonksiyonu - tek satırda çağır

    Örnek:
        results = search_products(driver, "laptop", "//input[@id='search']", "//div[@class='product']")
    """
    utils = AdvancedSearchUtils(driver)
    return utils.search_and_get_products(search_term, search_box, product_list)


def get_product(driver: WebDriver,
               product_locator: Union[str, Tuple[By, str]]) -> ProductDetail:
    """
    Tek ürün detayını çek - tek satırda çağır

    Örnek:
        product = get_product(driver, "//div[@class='product-detail']")
    """
    utils = AdvancedSearchUtils(driver)
    return utils.get_product_details(product_locator)


def extract_all_products(driver: WebDriver,
                        products_locator: Union[str, Tuple[By, str]],
                        max_products: int = 10) -> List[ProductDetail]:
    """
    Sayfadaki tüm ürünleri çek

    Örnek:
        products = extract_all_products(driver, "//div[contains(@class, 'product-item')]")
    """
    utils = AdvancedSearchUtils(driver)
    by, value = utils._parse_locator(products_locator)

    products = []
    elements = driver.find_elements(by, value)

    for i, element in enumerate(elements[:max_products], 1):
        print(f"Ürün {i} çekiliyor...")
        product = utils.extractor.extract_from_element(element)
        products.append(product)

    return products


# ÖRNEK KULLANIMLAR
if __name__ == "__main__":
    print("📚 AdvancedSearchUtils sınıfı başarıyla yüklendi")
    print("\nÖRNEK KULLANIM:")
    print("-" * 50)
    print("""
# 1. Basit arama:
results = search_products(
    driver, 
    "laptop", 
    "//input[@id='search']", 
    "//div[@class='product-item']"
)

# 2. Tek ürün detayı:
product = get_product(driver, "//div[@class='product-detail']")

# 3. Gelişmiş kullanım:
utils = AdvancedSearchUtils(driver)
results = utils.search_and_get_products(
    search_term="telefon",
    search_box_locator="//input[@name='q']",
    product_list_locator="//div[contains(@class, 'product-card')]",
    max_products=20
)

# 4. JSON kaydet:
utils.save_products_to_json(results)

# 5. Ürün detaylarını görüntüle:
for product in results.products[:3]:
    utils.print_product_details(product)
    """)