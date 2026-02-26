from pages.GeekPage import GeekPage, geekMail, geekPassword


def test_geek():
    geekPage=GeekPage()
    geekPage.navi_geek_home()
    geekPage.navi_geek_login()
    geekPage.geek_login_procudere(geekMail, geekPassword)
    geekPage.close_driver()

