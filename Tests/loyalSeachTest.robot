*** Settings ***
Documentation     LoyalFriend sitesinde Data Driven (Veri Odaklı) arama testi.
...               Bu test, LoyalFriendPage.py kütüphanesini kullanarak
...               farklı kelimelerle arama yapar ve sonuçları konsola yazdırır.

Library           ../pages/LoyalFriendPage.py    WITH NAME    LoyalPage
# Not: Library import ederken __init__ metodundaki driver argümanı sorun olabilir.
# Robot Framework, Python class'larını başlatırken argüman bekliyorsa (bizim __init__ driver istiyor),
# bunu yönetmek gerekir. Ancak en temiz yöntem, Page class'ını Robot uyumlu hale getirmektir.
# Şimdilik, LoyalFriendPage.py dosyasını Robot Framework'ün doğrudan başlatabileceği
# (driver'ı kendi içinde yöneten) bir yapıya sahip olduğunu varsayarak veya
# SeleniumLibrary kullanarak ilerleyebiliriz.
#
# Ancak mevcut LoyalFriendPage.py, __init__ metodunda 'driver' istiyor.
# Robot Framework bunu otomatik sağlayamaz.
# Bu yüzden bu dosya için 'SeleniumLibrary' kullanıp, Page fonksiyonlarını
# keyword olarak çağırmak daha sağlıklı olacaktır.
# VEYA LoyalFriendPage.py içinde küçük bir düzenleme ile Robot uyumluluğu artırılabilir.
#
# AŞAĞIDAKİ YAPI, MEVCUT LoyalFriendPage.py İLE ÇALIŞMAYABİLİR ÇÜNKÜ __init__ DRIVER İSTİYOR.
# BU NEDENLE, BU TESTİ ÇALIŞTIRMADAN ÖNCE LoyalFriendPage.py'DE KÜÇÜK BİR DÜZENLEME YAPACAĞIZ.

Library           SeleniumLibrary

Test Setup        Open Browser To Home Page
Test Teardown     Close Browser
Test Template     Urun Arama Senaryosu

*** Variables ***
${URL}      https://qa.loyalfriendcare.com/en
${BROWSER}  Chrome

*** Test Cases ***            ARAMA_TERIMI
Re Arama Testi                re
Ra Arama Testi                ra
Dog Arama Testi               dog
Cat Arama Testi               cat
Olmayan Urun Arama Testi      nonexistentproduct

*** Keywords ***
Open Browser To Home Page
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window

Urun Arama Senaryosu
    [Arguments]    ${arama_terimi}
    # Burada Python tarafındaki mantığı Robot keywordleri ile simüle ediyoruz
    # Veya Python class'ını düzelttikten sonra direkt Python keywordlerini çağırabiliriz.
    # Şimdilik SeleniumLibrary ve Python utils karışık hibrit bir yapı kuralım:

    Wait Until Element Is Visible    xpath=//input[@class="form-control"]
    Input Text    xpath=//input[@class="form-control"]    ${arama_terimi}
    Press Keys    xpath=//input[@class="form-control"]    RETURN

    # Sonuçların gelmesini bekle (Ürün ismi veya 'bulunamadı' durumu)
    Sleep    2s

    # Sonuçları logla (Basit kontrol)
    Log To Console    \n--- Arama Yapıldı: ${arama_terimi} ---
    ${count}=    Get Element Count    xpath=//div[@class="wrapper"]//h3
    Log To Console    Bulunan Urun Sayisi: ${count}

    Run Keyword If    ${count} > 0    Listele Urun Isimleri
    Log To Console    ------------------------------------

Listele Urun Isimleri
    @{elements}=    Get WebElements    xpath=//div[@class="wrapper"]//h3
    FOR    ${element}    IN    @{elements}
        ${text}=    Get Text    ${element}
        Log To Console    Urun: ${text}
    END
