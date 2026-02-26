"""
Search Utilities - Arama işlemleri için yardımcı sınıf
Author: QA Engineer
Date: 2024
"""

import time
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


@dataclass
class SearchResult:
    """Arama sonucu veri sınıfı"""
    term: str
    product_count: int
    products: List[Dict]
    search_time: float
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def summary(self) -> str:
        """Sonuç özeti döndürür"""
        return f"'{self.term}' için {self.product_count} ürün ({self.search_time:.2f}s)"


class SearchUtils:
    """
    Arama işlemleri için profesyonel yardımcı sınıf
    Tüm projelerde kullanılabilir, genel yapı
    """

    # Varsayılan XPath'ler
    DEFAULT_SEARCH_BOX = '//input[@type="search" or contains(@class, "search") or @name="search" or @id="search"]'
    DEFAULT_PRODUCT_WRAPPER = '//*[contains(@class, "product") or contains(@class, "item") or contains(@class, "wrapper")]'
    DEFAULT_PRODUCT_TITLE = './/h4 | .//h3 | .//*[contains(@class, "title")] | .//*[contains(@class, "name")]'

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        SearchUtils sınıfı başlatıcı

        Args:
            driver: Selenium WebDriver instance
            timeout: Varsayılan bekleme süresi (saniye)
        """
        self.driver = driver
        self.timeout = timeout
        self.search_history: List[SearchResult] = []
        self.report_dir = self._create_report_directory()

    def _create_report_directory(self) -> Path:
        """Raporlar için dizin oluşturur"""
        report_dir = Path.cwd() / "test_reports" / "search_results"
        report_dir.mkdir(parents=True, exist_ok=True)
        return report_dir

    def _wait_for_element(self, by: By, value: str, timeout: Optional[int] = None) -> Optional[object]:
        """
        Elementin görünmesini bekler

        Args:
            by: By tipi (By.XPATH, By.ID, etc.)
            value: Element lokasyonu
            timeout: Özel bekleme süresi

        Returns:
            WebElement veya None
        """
        try:
            wait_time = timeout or self.timeout
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            print(f"⚠️ Element bulunamadı: {value}")
            return None

    def search_and_get_results(self,
                               search_term: str,
                               search_box_xpath: Optional[str] = None,
                               product_wrapper_xpath: Optional[str] = None,
                               product_title_xpath: Optional[str] = None,
                               wait_after_search: int = 3,
                               clear_before_search: bool = True,
                               max_products_to_extract: int = 100) -> SearchResult:
        """
        Arama yapar ve sonuçları döndürür

        Args:
            search_term: Aranacak kelime
            search_box_xpath: Arama kutusu XPath'i (None = varsayılan)
            product_wrapper_xpath: Ürün wrapper XPath'i (None = varsayılan)
            product_title_xpath: Ürün başlık XPath'i (None = varsayılan)
            wait_after_search: Arama sonrası bekleme süresi
            clear_before_search: Aramadan önce kutuyu temizle
            max_products_to_extract: Çekilecek maksimum ürün sayısı

        Returns:
            SearchResult objesi
        """
        start_time = time.time()

        # XPath'leri belirle
        search_xpath = search_box_xpath or self.DEFAULT_SEARCH_BOX
        wrapper_xpath = product_wrapper_xpath or self.DEFAULT_PRODUCT_WRAPPER
        title_xpath = product_title_xpath or self.DEFAULT_PRODUCT_TITLE

        products_found = []

        try:
            # Arama kutusunu bul ve temizle
            search_box = self._wait_for_element(By.XPATH, search_xpath)
            if not search_box:
                raise Exception(f"Arama kutusu bulunamadı: {search_xpath}")

            if clear_before_search:
                search_box.clear()

            # Arama yap
            search_box.send_keys(search_term)
            search_box.submit()

            # Sonuçların yüklenmesini bekle
            time.sleep(wait_after_search)

            # Ürün wrapperlarını bul
            wrappers = self.driver.find_elements(By.XPATH, wrapper_xpath)

            # Ürün bilgilerini çek
            for i, wrapper in enumerate(wrappers[:max_products_to_extract], 1):
                product_info = self._extract_product_info(wrapper, i, title_xpath)
                if product_info:
                    products_found.append(product_info)

        except Exception as e:
            print(f"❌ Arama sırasında hata: {e}")

        # Arama sonucu oluştur
        search_time = time.time() - start_time
        result = SearchResult(
            term=search_term,
            product_count=len(products_found),
            products=products_found,
            search_time=search_time
        )

        # Geçmişe ekle
        self.search_history.append(result)

        return result

    def _extract_product_info(self, wrapper, index: int, title_xpath: str) -> Optional[Dict]:
        """
        Tek bir ürünün bilgilerini çıkarır

        Args:
            wrapper: WebElement
            index: Ürün indeksi
            title_xpath: Başlık XPath'i

        Returns:
            Ürün bilgileri sözlüğü veya None
        """
        try:
            # Başlığı bulmaya çalış
            title_element = None
            title_text = None

            # Ana XPath ile dene
            try:
                title_element = wrapper.find_element(By.XPATH, title_xpath)
                title_text = title_element.text.strip()
            except:
                pass

            # Eğer bulunamazsa wrapper'ın kendi text'ini dene
            if not title_text:
                title_text = wrapper.text.strip()

            # Hala boşsa None döndür
            if not title_text:
                return None

            # Fiyat bilgisini dene (varsa)
            price = None
            try:
                price_element = wrapper.find_element(By.XPATH,
                                                     './/*[contains(@class, "price") or contains(@class, "fiyat")]')
                price = price_element.text.strip()
            except:
                pass

            # Link bilgisini dene (varsa)
            link = None
            try:
                link_element = wrapper.find_element(By.XPATH, './/a')
                link = link_element.get_attribute('href')
            except:
                pass

            return {
                'index': index,
                'name': title_text,
                'price': price,
                'link': link,
                'element': wrapper  # İleri seviye işlemler için
            }

        except Exception as e:
            print(f"  ⚠️ Ürün {index} bilgisi alınamadı: {e}")
            return None

    def print_results(self, result: SearchResult, show_details: bool = True, max_show: int = 10):
        """
        Arama sonuçlarını ekrana yazdırır

        Args:
            result: SearchResult objesi
            show_details: Detayları göster
            max_show: Gösterilecek maksimum ürün sayısı
        """
        print("\n" + "=" * 70)
        print(f"🔍 ARAMA SONUCU: '{result.term}'")
        print("=" * 70)
        print(f"⏱️  Süre: {result.search_time:.2f} saniye")
        print(f"📦 Toplam ürün: {result.product_count}")
        print(f"🕐 Zaman: {result.timestamp}")

        if show_details and result.products:
            print("\n📋 ÜRÜN LİSTESİ:")
            print("-" * 70)

            for product in result.products[:max_show]:
                price_str = f" - 💰 {product['price']}" if product['price'] else ""
                print(f"{product['index']:3d}. {product['name'][:70]}{price_str}")

            if result.product_count > max_show:
                print(f"\n   ... ve {result.product_count - max_show} ürün daha")

        print("=" * 70)

    def save_report(self, result: SearchResult, filename: Optional[str] = None) -> Path:
        """
        Arama sonuçlarını dosyaya kaydeder

        Args:
            result: SearchResult objesi
            filename: Özel dosya adı (None = otomatik)

        Returns:
            Kaydedilen dosya yolu
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_{result.term}_{timestamp}.txt"

        file_path = self.report_dir / filename

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write(f"ARAMA RAPORU: '{result.term}'\n")
                f.write("=" * 70 + "\n")
                f.write(f"Tarih: {result.timestamp}\n")
                f.write(f"Süre: {result.search_time:.2f} saniye\n")
                f.write(f"Toplam Ürün: {result.product_count}\n")
                f.write("-" * 70 + "\n\n")

                if result.products:
                    f.write("ÜRÜN LİSTESİ:\n")
                    f.write("-" * 70 + "\n")

                    for product in result.products:
                        f.write(f"{product['index']:3d}. {product['name']}\n")
                        if product['price']:
                            f.write(f"      Fiyat: {product['price']}\n")
                        if product['link']:
                            f.write(f"      Link: {product['link']}\n")
                        f.write("-" * 40 + "\n")

                f.write("\n" + "=" * 70 + "\n")
                f.write("RAPOR SONU\n")
                f.write("=" * 70 + "\n")

            print(f"💾 Rapor kaydedildi: {file_path}")
            return file_path

        except Exception as e:
            print(f"❌ Rapor kaydedilemedi: {e}")
            return file_path

    def compare_searches(self, *terms: str) -> Dict:
        """
        Farklı arama terimlerini karşılaştırır

        Args:
            *terms: Karşılaştırılacak terimler

        Returns:
            Karşılaştırma sonuçları
        """
        comparison = {}

        for term in terms:
            # Geçmişte var mı kontrol et
            existing = next((r for r in self.search_history if r.term == term), None)

            if existing:
                comparison[term] = {
                    'count': existing.product_count,
                    'time': existing.search_time,
                    'products': existing.products[:5]  # İlk 5 ürün
                }
            else:
                # Yoksa yeni arama yap
                result = self.search_and_get_results(term)
                comparison[term] = {
                    'count': result.product_count,
                    'time': result.search_time,
                    'products': result.products[:5]
                }

        return comparison

    def get_statistics(self) -> Dict:
        """
        Arama istatistiklerini döndürür
        """
        if not self.search_history:
            return {"message": "Henüz arama yapılmadı"}

        total_searches = len(self.search_history)
        total_products = sum(r.product_count for r in self.search_history)
        avg_products = total_products / total_searches
        avg_time = sum(r.search_time for r in self.search_history) / total_searches

        return {
            "total_searches": total_searches,
            "total_products": total_products,
            "average_products_per_search": round(avg_products, 2),
            "average_search_time": round(avg_time, 2),
            "most_productive_search": max(self.search_history, key=lambda x: x.product_count).term,
            "fastest_search": min(self.search_history, key=lambda x: x.search_time).term
        }

    def clear_history(self):
        """Arama geçmişini temizler"""
        self.search_history.clear()
        print("🧹 Arama geçmişi temizlendi")


# Kullanım kolaylığı için yardımcı fonksiyonlar
def create_search_utils(driver: WebDriver, timeout: int = 10) -> SearchUtils:
    """SearchUtils instance'ı oluşturur"""
    return SearchUtils(driver, timeout)


# Örnek kullanım
if __name__ == "__main__":
    # Test amaçlı örnek
    print("📚 SearchUtils sınıfı başarıyla yüklendi")
    print("Kullanım için: from utils.search_utils import SearchUtils")