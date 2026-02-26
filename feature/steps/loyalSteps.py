from behave import given, when

from pages.GeekPage import GeekPage
from pages.LoyalFriendCarePage import loyalmail, loyalpassword, LoyalFriendCarePage


@given(u'Kullanici loyalFriendCare ana sayfasina gider')
def step_impl(context):
    context.loyalFriendCarePage = LoyalFriendCarePage()
    context.loyalFriendCarePage.navi_loyal_home()

@when(u'Kullanici signUpButton a tiklar')
def step_impl(context):
    context.loyalFriendCarePage.navi_loyal_login()

@when(u'Kullanici login islemlerini gerceklestirir')
def step_impl(context):
    context.loyalFriendCarePage.loyal_login_procudere(loyalmail, loyalpassword)


@when(u'Kullanici tarayiciyi kapatir')
def step_impl(context):
    context.loyalFriendCarePage.close_driver()
