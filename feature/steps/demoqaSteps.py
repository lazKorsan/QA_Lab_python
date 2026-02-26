from behave import given, then

from pages.DemoqaPage import DemoqaPage, demoqaUserName, demoqaPassword


@given(u'demoqa kullanici ana sayfaya gider')
def step_impl(context):

    context.demoqaPage=DemoqaPage()
    context.demoqaPage.navi_demoqa_home()




@then(u'demoqa kullanicisi login sayfasina gider')
def step_impl(context):
    context.demoqaPage.navi_demoqa_login()



@then(u'demoqa kullanicisi login islemlerini gerceklesitririr')
def step_impl(context):
    context.demoqaPage.demoqa_login_procudure(demoqaUserName,demoqaPassword)



@then(u'demoqa kullanicisi tarayiciyici kapatir')
def step_impl(context):
    context.demoqaPage.close_driver()

