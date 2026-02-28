from behave import given, when, then
from LoyalTests.OK_beginnerLevel4 import navi_loyal_home, search_progress, list_products

@given('kullanıcı loyalfriendcare sayfasına gider')
def step_given_user_navigates_to_loyalfriendcare(context):
    navi_loyal_home()

@when('arama kutusunda "{search_terms}" aratır')
def step_when_user_searches(context, search_terms):
    search_list = search_terms.split(", ")
    for term in search_list:
        search_progress(term)

@then('sonuçları listeler')
def step_then_user_lists_results(context):
    list_products()
