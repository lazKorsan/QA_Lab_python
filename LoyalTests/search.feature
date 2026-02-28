Feature: Loyal Friend Care Arama Özelliği

  Scenario: : Kullanıcı ürün araması yapar
    Given  kullanıcı loyalfriendcare sayfasına gider
    Then  arama kutusunda "re, re, dog" aratır
    And Sonuçları listeler
