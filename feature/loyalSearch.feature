Feature:

  Scenario Outline:
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