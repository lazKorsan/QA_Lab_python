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