from behave import given, then
from robot.api.deco import keyword

from pages.GeekPage import GeekPage, geekMail, geekPassword

@keyword(u'Given Kullanici geekHomePage sayfasina gider')
@given(u'Kullanici geekHomePage sayfasina gider')
def step_impl(context):
    context.geekPages=GeekPage()
    context.geekPages.navi_geek_home()


keyword(u'Then Kullanici geekLoginPage sayfasina gider')
@then(u'Kullanici geekLoginPage sayfasina gider')
def step_impl(context):
    context.geekPages.navi_geek_login()
keyword(u'And Kullanici login islemlerini gerceklesitirir')
@then(u'Kullanici login islemlerini gerceklesitirir')
def step_impl(context):
    context.geekPages.geek_login_procudere(geekMail, geekPassword)
keyword(u'And Kullanici tarayiciyi kapatir')
@then(u'Kullanici tarayiciyi kapatir')
def step_impl(context):
    context.geekPages.close_driver()