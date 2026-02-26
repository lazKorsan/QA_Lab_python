import pytest
from selenium import webdriver
from pages.LoyalFriendPage import LoyalFriendPage # Yeni oluşturduğumuz Page Object'i import ediyoruz

@pytest.fixture(scope="module")
def driver():
    """Tüm testler için tek bir tarayıcı örneği sağlar."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.parametrize("search_term", [
    "re",
    "ra",
    "dog",
    "cat",
    "nonexistentproduct" # Ürün bulunamayan bir senaryo için
])
def test_loyalfriend_search_with_pom(driver, search_term):
    """
    LoyalFriend sitesinde Page Object Model kullanarak arama testi.
    Test adımları LoyalFriendPage sınıfı metotları ile yönetilir.
    """
    # 1. Page Object'in bir örneğini oluştur
    loyal_page = LoyalFriendPage(driver)

    # 2. Ana sayfaya git
    loyal_page.navigate_to_home()

    # 3. Ürün ara
    loyal_page.search_product(search_term)

    # 4. Arama sonuçlarını yazdır
    loyal_page.print_product_info(search_term)

    # İsteğe bağlı: Burada ürün sayısını veya isimlerini assert edebilirsiniz.
    # Örneğin:
    # if search_term == "re":
    #     assert loyal_page.get_product_count() > 0
    # elif search_term == "nonexistentproduct":
    #     assert loyal_page.get_product_count() == 0
