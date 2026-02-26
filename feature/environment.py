from selenium import webdriver
from pages.LoyalFriendPage import LoyalFriendPage

def before_all(context):
    """Tüm feature'lar başlamadan önce çalışır."""
    context.driver = webdriver.Chrome()
    context.driver.maximize_window()
    context.loyal_page = LoyalFriendPage(context.driver) # LoyalFriendPage instance'ını burada oluştur

def after_all(context):
    """Tüm feature'lar bittikten sonra çalışır."""
    if context.driver:
        context.driver.quit()

def before_scenario(context, scenario):
    """Her senaryo başlamadan önce çalışır."""
    # Her senaryo için ana sayfaya gitmek, tarayıcıyı kapatıp açmaktan daha hızlıdır.
    context.loyal_page.navigate_to_home()

# after_scenario'ya gerek yok çünkü driver'ı her senaryo için kapatmıyoruz.
# before_scenario'da ana sayfaya giderek her senaryo için temiz bir başlangıç sağlıyoruz.
