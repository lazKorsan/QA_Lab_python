# language: tr
Feature: LoyalFriend Ürün Arama Fonksiyonu

  Kullanıcıların LoyalFriend web sitesinde ürün arama özelliğini
  doğru bir şekilde kullanabildiğini doğrulamak.

  Scenario Outline: Kullanıcı sitede bir ürün arar ve sonuçları görür
    Given Kullanıcı LoyalFriend ana sayfasındadır
    When Kullanıcı arama kutusuna "<arama_terimi>" yazar ve arar
    Then Arama sonuçlarında bulunan ürün sayısı ve listesi konsola yazdırılır

    Examples:
      | arama_terimi       |
      | re                 |
      | ra                 |
      | dog                |
      | cat                |
      | nonexistentproduct |
