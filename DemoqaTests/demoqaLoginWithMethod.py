from pages.DemoqaPage import DemoqaPage, demoqaUserName, demoqaPassword


def test_demoqa_login_method():
    demoqaPage = DemoqaPage()
    demoqaPage.navi_demoqa_home()
    demoqaPage.navi_demoqa_login()
    demoqaPage.demoqa_login_procudure(demoqaUserName, demoqaPassword)
    demoqaPage.close_driver()