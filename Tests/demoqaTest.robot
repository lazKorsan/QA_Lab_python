*** Settings ***
Library    ../pages/DemoqaPage.py

*** Variables ***
${BROWSER}    chrome
${userName}    LazKorsan
${password}    Query.2026!

*** Test Cases ***
demoqa robot testi
    demoqa ana sayfasina gider    ${BROWSER}
    demoqa login sayfasina gider    ${BROWSER}
    login islemlerini gerceklesitirir    ${userName}    ${password}
    demoqa tarayiciyi kapatir