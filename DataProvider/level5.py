import time
import pytest
from selenium import webdriver
from utils.search_utils import SearchUtils, create_search_utils


class TestSearch:
    """SearchUtils kullanım örneği"""

    @pytest.fixture
    def search_utils(self):
        """SearchUtils fixture'ı"""
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://qa.loyalfriendcare.com/en")

        # SearchUtils oluştur
        utils = SearchUtils(driver, timeout=10)

        yield utils

        # Temizlik
        utils.driver.quit()

    def test_single_search(self, search_utils):
        """Tek arama testi"""
        # Basit arama
        result = search_utils.search_and_get_results(
            search_term="re",
            wait_after_search=3
        )

        # Sonuçları göster
        search_utils.print_results(result)

        # Rapor kaydet
        search_utils.save_report(result)

        # Assertion
        assert result.product_count > 0

    @pytest.mark.parametrize("term", ["re", "ra", "do", "ca"])
    def test_multiple_searches(self, search_utils, term):
        """Çoklu arama testi"""
        result = search_utils.search_and_get_results(
            search_term=term,
            wait_after_search=2
        )

        print(f"\n📊 {term}: {result.product_count} ürün")
        assert result.product_count > 0

    def test_advanced_search(self, search_utils):
        """Gelişmiş arama testi"""
        # Özel XPath'ler ile arama
        result = search_utils.search_and_get_results(
            search_term="re",
            search_box_xpath='//input[@class="form-control"]',
            product_wrapper_xpath='//*[@class="wrapper"]',
            product_title_xpath='.//h4',
            max_products_to_extract=50
        )

        # Detaylı gösterim
        search_utils.print_results(result, show_details=True, max_show=15)

        # Rapor kaydet
        search_utils.save_report(result, "ozel_rapor.txt")

    def test_compare_searches(self, search_utils):
        """Arama karşılaştırma testi"""
        # Önce birkaç arama yap
        search_utils.search_and_get_results("re")
        search_utils.search_and_get_results("ra")
        search_utils.search_and_get_results("do")

        # Karşılaştır
        comparison = search_utils.compare_searches("re", "ra", "do", "ca")

        print("\n📊 ARAMA KARŞILAŞTIRMASI:")
        for term, data in comparison.items():
            print(f"  {term}: {data['count']} ürün ({data['time']:.2f}s)")

        # İstatistikler
        stats = search_utils.get_statistics()
        print("\n📈 İSTATİSTİKLER:")
        for key, value in stats.items():
            print(f"  {key}: {value}")