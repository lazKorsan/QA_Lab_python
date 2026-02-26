

*** Settings ***
Library    ../pages/LoyalFriendCarePage.py

*** Variables ***
${BROWSER}    chrome
${mail}    jlazKorsan190220262054@gmail.com
${password}    Query.2026!

*** Test Cases ***
loyalfriendcare sitesi login testi
    loyalFriendCare sayfasina gider
    loyalfriendCareLogin sayfasina gider
    loyalfriendCare login islemlerini gerceklesitirir    ${mail}    ${password}
    loyalfriendCare tarayiciyi kapatir