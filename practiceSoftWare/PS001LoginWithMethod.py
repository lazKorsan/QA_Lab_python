from lib2to3.pgen2 import driver

from pages.soft_ware_test_page import PracticeSoftWarePage, practice_software_email, practice_software_password


def test_paractice_soft_ware():
    page = PracticeSoftWarePage()
    page.go_to_practice_test_homepage()
    page.navigate_to_login_page()
    page.login_procudere(practice_software_email, practice_software_password)
    page.close_driver()






