from pages.LoyalFriendCarePage import LoyalFriendCarePage, loyalmail, loyalpassword


def test_loyal():
    loyalFriendCarePage = LoyalFriendCarePage()
    loyalFriendCarePage.navi_loyal_home()
    loyalFriendCarePage.navi_loyal_login()
    loyalFriendCarePage.loyal_login_procudere(loyalmail, loyalpassword)
    loyalFriendCarePage.close_driver()