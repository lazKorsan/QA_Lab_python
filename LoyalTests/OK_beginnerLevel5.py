import pytest
from LoyalTests.OK_beginnerLevel4 import navi_loyal_home, search_progress, list_products, setup_driver


@pytest.mark.parametrize("searchList", ["re", "ra"])
def test_search_test_loyal(setup_driver, searchList):
    # setup_driver fixture'ı burada otomatik olarak çağrılacak
    navi_loyal_home()  # Ana sayfaya git
    search_progress(searchList)  # Arama yap
    list_products()  # Ürünleri listele
