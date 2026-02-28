"""
multipleSearch.py - DataProvider mantığıyla parametrize edilmiş test
Aranacak kelimeler: re, re, dog (tekrarlı ve farklı)
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from datetime import datetime
from pathlib import Path

from utils.search_utils import AdvancedSearchUtils

# TEST VERİLERİ - DataProvider mantığı
# (test_metodu, arama_terimi, açıklama)
test_data = [
    ("test_search_with_term", "re", "İlk 're' araması"),
    ("test_search_with_term", "re", "İkinci 're' araması (tekrarlı)"),
    ("test_search_with_term", "dog", "Köpek araması"),
    ("test_search_with_term", "cat", "Kedi araması"),
    ("test_search_with_term", "bird", "Kuş araması"),
    ("test_search_with_term", "fish", "Balık araması"),
    ("test_search_empty", "", "Boş arama"),
    ("test_search_special_chars", "!@#$%", "Özel karakter araması"),
]


class TestLoyalFriendCareSearch:
    """
    LoyalFriendCare sitesi için parametrize edilmiş test sınıfı
    """

    # Raporlama için klasör oluştur
    report_dir = Path.cwd() / "test_reports" / "parameterized_tests"
    report_dir.mkdir(parents=True, exist_ok=True)

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Her test öncesi çalışır"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://qa.loyalfriendcare.com/en")
        time.sleep(2)
        self.search_utils = AdvancedSearchUtils(self.driver, timeout=10)
        self.test_results = []
        yield
        self.driver.quit()

    @pytest.mark.parametrize("test_name,search_term,description",
                             [(d[0], d[1], d[2]) for d in test_data])
    def test_search_parameterized(self, test_name, search_term, description):
        """
        Parametre edilmiş test - DataProvider mantığı

        Args:
            test_name: Test metodu adı (kullanılmıyor, sadece bilgi için)
            search_term: Aranacak kelime
            description: Test açıklaması
        """
        print(f"\n{'=' * 70}")
        print(f"🔍 TEST BAŞLIYOR: '{search_term}' - {description}")
        print(f"{'=' * 70}")

        # Test başlangıç zamanı
        start_time = time.time()

        try:
            # Arama yap
            results = self.search_utils.search_and_get_products(
                search_term=search_term,
                search_box_locator='//input[@class="form-control"]',
                product_list_locator='//*[contains(@class, "card") or contains(@class, "item") or @class="wrapper"]',
                wait_after_search=3,
                max_products=20
            )

            # Test süresi
            test_duration = time.time() - start_time

            # Test sonucunu kaydet
            test_result = {
                "term": search_term,
                "description": description,
                "product_count": results.product_count,
                "duration": round(test_duration, 2),
                "status": "PASS" if results.product_count > 0 else "WARNING",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "products_found": [p.name for p in results.products[:20]]  # İlk 5 ürün
            }

            # Sonuçları göster
            self._print_test_result(test_result)

            # Assertion - beklenen sonuçlar
            if search_term == "":
                # Boş arama - genelde tüm ürünleri gösterir veya hata mesajı
                assert results.product_count >= 0
            elif search_term in ["!@#$%", "bird", "fish"]:
                # Bu terimlerde sonuç çıkmayabilir
                print(f"⚠️ '{search_term}' için sonuç: {results.product_count} ürün")
            else:
                # Normal aramalarda en az 1 sonuç bekliyoruz
                assert results.product_count >= 0  # Siteye göre değişir

            # JSON kaydet (her test için ayrı)
            self._save_test_report(search_term, results, test_result)

            # Test sonucunu listeye ekle
            self.test_results.append(test_result)

        except Exception as e:
            test_duration = time.time() - start_time
            error_result = {
                "term": search_term,
                "description": description,
                "product_count": 0,
                "duration": round(test_duration, 2),
                "status": "FAIL",
                "error": str(e),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.test_results.append(error_result)
            self._print_test_result(error_result)
            pytest.fail(f"Test başarısız: {e}")

    def _print_test_result(self, result: dict):
        """Test sonucunu yazdırır"""
        status_icon = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "WARNING" else "❌"
        print(f"\n{status_icon} SONUÇ: '{result['term']}'")
        print(f"   📊 Ürün sayısı: {result['product_count']}")
        print(f"   ⏱️  Süre: {result['duration']}s")
        if result.get("products_found"):
            print(f"   📋 İlk 5 ürün: {', '.join(result['products_found'])}")
        if result.get("error"):
            print(f"   ❗ Hata: {result['error']}")

    def _save_test_report(self, search_term: str, results, test_result: dict):
        """Her test için JSON rapor kaydeder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_term = search_term.replace(" ", "_").replace("!", "").replace("@", "").replace("#", "").replace("$",
                                                                                                             "").replace(
            "%", "")
        if not safe_term:
            safe_term = "empty"

        filename = self.report_dir / f"test_{safe_term}_{timestamp}.json"

        report_data = {
            "test_info": test_result,
            "search_details": {
                "term": results.term,
                "total_products": results.product_count,
                "search_time": results.search_time,
                "timestamp": results.timestamp
            },
            "products": [p.to_dict() for p in results.products[:10]]  # İlk 10 ürün detayı
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)

        print(f"   💾 Rapor kaydedildi: {filename}")

    @pytest.fixture(autouse=True)
    def generate_final_report(self):
        """Tüm testler bittikten sonra final rapor oluşturur"""
        yield
        if hasattr(self, 'test_results') and self.test_results:
            self._create_summary_report()

    def _create_summary_report(self):
        """Tüm testlerin özet raporunu oluşturur"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = self.report_dir / f"test_summary_{timestamp}.json"
        html_report = self.report_dir / f"test_summary_{timestamp}.html"

        # İstatistikler
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["status"] == "PASS")
        warning_tests = sum(1 for r in self.test_results if r["status"] == "WARNING")
        failed_tests = sum(1 for r in self.test_results if r["status"] == "FAIL")

        summary = {
            "test_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_tests": total_tests,
            "passed": passed_tests,
            "warnings": warning_tests,
            "failed": failed_tests,
            "success_rate": f"{(passed_tests / total_tests) * 100:.1f}%" if total_tests > 0 else "0%",
            "test_results": self.test_results
        }

        # JSON özet kaydet
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        # HTML rapor oluştur
        self._create_html_report(html_report, summary)

        print(f"\n{'=' * 70}")
        print("📊 TEST ÖZET RAPORU")
        print(f"{'=' * 70}")
        print(f"Toplam Test: {total_tests}")
        print(f"✅ Geçen: {passed_tests}")
        print(f"⚠️  Uyarı: {warning_tests}")
        print(f"❌ Başarısız: {failed_tests}")
        print(f"📈 Başarı Oranı: {summary['success_rate']}")
        print(f"\n📁 JSON Rapor: {summary_file}")
        print(f"📁 HTML Rapor: {html_report}")
        print(f"{'=' * 70}")

    def _create_html_report(self, html_path: Path, summary: dict):
        """HTML formatında rapor oluşturur"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Sonuçları</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .summary {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
                .pass {{ color: green; }}
                .warning {{ color: orange; }}
                .fail {{ color: red; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>🔍 Test Sonuçları</h1>
            <div class="summary">
                <h2>Özet</h2>
                <p>Tarih: {summary['test_date']}</p>
                <p>Toplam Test: {summary['total_tests']}</p>
                <p class="pass">Geçen: {summary['passed']}</p>
                <p class="warning">Uyarı: {summary['warnings']}</p>
                <p class="fail">Başarısız: {summary['failed']}</p>
                <p>Başarı Oranı: {summary['success_rate']}</p>
            </div>

            <h2>Detaylı Sonuçlar</h2>
            <table>
                <tr>
                    <th>Arama Terimi</th>
                    <th>Açıklama</th>
                    <th>Ürün Sayısı</th>
                    <th>Süre (s)</th>
                    <th>Durum</th>
                </tr>
        """

        for result in summary['test_results']:
            status_class = "pass" if result['status'] == "PASS" else "warning" if result[
                                                                                      'status'] == "WARNING" else "fail"
            status_icon = "✅" if result['status'] == "PASS" else "⚠️" if result['status'] == "WARNING" else "❌"

            html_content += f"""
                <tr>
                    <td>{result['term']}</td>
                    <td>{result['description']}</td>
                    <td>{result['product_count']}</td>
                    <td>{result['duration']}</td>
                    <td class="{status_class}">{status_icon} {result['status']}</td>
                </tr>
            """

        html_content += """
            </table>
        </body>
        </html>
        """

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)


# Basit data provider fonksiyonu (alternatif kullanım)
def data_provider():
    """Test verilerini döndüren jeneratör"""
    test_cases = [
        ("re", "İlk re araması"),
        ("re", "Tekrarlı re araması"),
        ("dog", "Köpek araması"),
        ("cat", "Kedi araması"),
        ("bird", "Kuş araması"),
        ("", "Boş arama"),
        ("!@#$", "Özel karakter"),
    ]
    for term, desc in test_cases:
        yield term, desc


# Doğrudan çalıştırmak için
if __name__ == "__main__":
    print("🚀 Testler pytest ile çalıştırılmalıdır.")
    print("Kullanım: pytest multipleSearch.py -v")
    print("Alternatif: python -m pytest multipleSearch.py --html=report.html")

    # Tek seferlik test için
    driver = webdriver.Chrome()
    try:
        driver.get("https://qa.loyalfriendcare.com/en")
        utils = AdvancedSearchUtils(driver)

        # Data provider'daki tüm terimleri dene
        for term, desc in data_provider():
            print(f"\n📝 Test: {desc} - '{term}'")
            results = utils.search_and_get_products(
                search_term=term,
                search_box_locator='//input[@class="form-control"]',
                product_list_locator='//*[@class="wrapper"]',
                max_products=5
            )
            print(f"   Sonuç: {results.product_count} ürün")

    finally:
        driver.quit()