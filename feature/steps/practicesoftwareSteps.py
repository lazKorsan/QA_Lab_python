from behave import given, then, when

from pages.PracticeSoftWarePage import practice_software_email, practice_software_password, PracticeSoftWarePage


@given(u'Kullanici practicesoftware sayfasina gider')
def step_impl(context):
    # Kullanici driver nesnesini olusturur
    context.practice_software_page = PracticeSoftWarePage()
    # Kullanici practice software sayfasina gider
    context.practice_software_page.go_to_practice_test_homepage()

@then(u'Kullanici login sayfasina gider')
# Kullanici login sayfasina gider
def step_impl(context):
    context.practice_software_page.navigate_to_login_page()

@then(u'Kullanici login islemlerini gerçeklestirir')
# Kullanici login islemlerini gerçekleştirir
def step_impl(context):
    context.practice_software_page.login_procudere(practice_software_email, practice_software_password)
    context.practice_software_page.close_driver()


@when(u'Kullanici dirver kapatir')
# Kullanici driver kapatir
def step_impl(context):
    context.practice_software_page.close_driver()