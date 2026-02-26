*** Settings ***
Library    ../pages/GeekPage.py

*** Variables ***
${BROWSER}    chrome
${mail}    jemote1577@pazuric.com
${password}    Query.2026!

*** Test Cases ***
geek sitesi login testi
    geekHomePage sayfasina gider    ${BROWSER}
    geekLoginPage sayfasina gider    ${BROWSER}
    login islemlerini gerceklesitirir    ${mail}    ${password}
    tarayiciyi kapatir    ${BROWSER}
