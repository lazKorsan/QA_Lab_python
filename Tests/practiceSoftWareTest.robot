
*** Settings ***
Library    ../pages/PracticeSoftWarePage.py

*** Variables ***
${BROWSER}    chrome
${mail}    lazKorsan123@gmail.com
${password}    Query.2026!

*** Test Cases ***
practiceSoftWare Login testi
    practicesoftware ana sayfasina gider    ${browser}
    practicesoftware login sayfasina gider    ${browser}
    practice software login islemlerini gerceklestirir    ${mail}    ${password}
    practicesoftware tarayiciyi kapatir
