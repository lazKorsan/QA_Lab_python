from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Doğru import - sınıfı içe aktarıyoruz
from utils.search_utils import AdvancedSearchUtils

# Driver'ı başlat
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # Siteye git
    driver.get("https://qa.loyalfriendcare.com/en")
    time.sleep(3)  # Sayfanın tam yüklenmesi için bekle

    print("🔍 Siteye gidiliyor...")

    # AdvancedSearchUtils instance'ı oluştur
    search_utils = AdvancedSearchUtils(driver, timeout=10)

    # Arama yap ve ürünleri listele
    print("\n🔎 Arama yapılıyor: 're'")

    # NOT: Bu sitede muhtemelen ürün listesi yok, servisler var.
    # O yüzden product_list_locator'ı servis kartlarına göre ayarladım.
    results = search_utils.search_and_get_products(
        search_term="re",
        search_box_locator='//input[@class="form-control"]',  # Arama kutusu
        product_list_locator='//*[@class="wrapper"]',
        # Servis/Ürün kartları
        wait_after_search=3,
        max_products=10  # Sitede çok fazla kart yoksa 10 yeterli
    )

    # Sonuçları ekrana yazdır
    print(f"\n📊 Toplam {results.product_count} öğe bulundu.")

    # İlk 3 ürünün detaylarını göster
    if results.products:
        print("\n" + "=" * 70)
        print("İLK 3 ÖĞENİN DETAYLARI")
        print("=" * 70)

        for i, product in enumerate(results.products[:3], 1):
            print(f"\n--- ÖĞE {i} ---")
            # Detayları yazdırmak için yardımcı metod
            print(f"📝 İsim: {product.name}")
            print(f"💰 Fiyat: {product.price or 'Belirtilmemiş'}")
            print(f"🔗 Link: {product.link or 'Yok'}")
            if product.description:
                print(f"📄 Açıklama: {product.description[:100]}...")

        # İlk ürünün tüm detaylarını detaylı göster
        print("\n" + "=" * 70)
        print("İLK ÖĞENİN TÜM DETAYLARI")
        search_utils.print_product_details(results.products[0], detailed=True)
    else:
        print("❌ Hiç öğe bulunamadı. Locator'ları kontrol edin.")

    # JSON olarak kaydet
    json_path = search_utils.save_products_to_json(results)
    print(f"\n💾 JSON dosyası: {json_path}")

    # Rapor olarak kaydet (düz metin)
    report_path = search_utils.report_dir / f"report_{results.term}.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"Arama Terimi: {results.term}\n")
        f.write(f"Toplam Öğe: {results.product_count}\n")
        f.write(f"Süre: {results.search_time:.2f}s\n\n")
        for p in results.products:
            f.write(f"- {p.name}\n")
    print(f"💾 Rapor kaydedildi: {report_path}")

    # İstatistikleri göster
    if search_utils.search_history:
        stats = search_utils.get_statistics()
        print("\n📈 ARAMA İSTATİSTİKLERİ:")
        for key, value in stats.items():
            print(f"   {key}: {value}")

except Exception as e:
    print(f"❌ Hata oluştu: {e}")

finally:
    # Tarayıcıyı kapat (test bittiğinde)
    print("\n🏁 Test tamamlandı, tarayıcı kapatılıyor...")
    time.sleep(2)
    driver.quit()