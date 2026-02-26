# SearchUtils oluştur
from DataProvider.level1 import driver
from utils.search_utils import SearchUtils

utils = SearchUtils(driver)

# Arama yap
result = utils.search_and_get_results("re")

# Sonuçları göster
utils.print_results(result)

# Rapor kaydet
utils.save_report(result)