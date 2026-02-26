from behave import given, when, then

# Not: driver ve loyal_page nesneleri environment.py dosyasında context'e eklenmiştir.

@given('Kullanıcı LoyalFriend ana sayfasındadır')
def step_given_user_on_homepage(context):
    """
    Bu adım environment.py'deki before_scenario tarafından zaten gerçekleştiriliyor.
    Yine de senaryonun okunabilirliği için bu adımı burada tanımlıyoruz.
    İsteğe bağlı olarak burada ek bir kontrol (örneğin, sayfa başlığını doğrulamak) yapılabilir.
    """
    print("✅ Kullanıcı ana sayfada.")
    # context.loyal_page.navigate_to_home() # Bu satır environment.py'de olduğu için burada tekrar çağırmaya gerek yok.
    pass

@when('Kullanıcı arama kutusuna "{arama_terimi}" yazar ve arar')
def step_when_user_searches(context, arama_terimi):
    """
    Kullanıcı verilen arama terimini kullanarak arama yapar.
    """
    context.arama_terimi = arama_terimi # Sonraki adımda kullanmak için arama terimini context'e kaydet
    context.loyal_page.search_product(arama_terimi)

@then('Arama sonuçlarında bulunan ürün sayısı ve listesi konsola yazdırılır')
def step_then_print_results(context):
    """
    Arama sonuçlarını alır ve konsola yazdırır.
    """
    context.loyal_page.print_product_info(context.arama_terimi)
