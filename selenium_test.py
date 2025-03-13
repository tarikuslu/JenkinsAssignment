from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chrome seçeneklerini ayarla (başsız modda çalışsın)
chrome_options = Options()
chrome_options.add_argument("--headless")  # GUI olmadan çalışır
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# WebDriver'ı başlat
driver = webdriver.Chrome(options=chrome_options)

try:
    # 1. LC Waikiki sitesine git
    driver.get("https://www.lcwaikiki.com/tr-TR/TR")
    print("Siteye gidildi: " + driver.title)

    # Assertion: Sayfanın başlığını kontrol et
    expected_title = "LCW.com: Trendler ve Yenilikçi Online Alışveriş Deneyimi Burada! | LCW"
    assert expected_title in driver.title, f"Başlık '{expected_title}' içermiyor! Bulunan: {driver.title}"
    print("Başlık doğrulandı!")

    # 2. "Kategoriler" menüsüne tıkla
    kategoriler_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Kategoriler')]"))
    )
    kategoriler_button.click()
    print("Kategoriler menüsüne tıklandı!")

    # 3. "Erkek" kategorisini seç
    erkek_kategori = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Erkek')]"))
    )
    erkek_kategori.click()
    print("Erkek kategorisi seçildi!")

    # 4. Arama çubuğuna "gömlek" yaz ve ara
    arama_cubugu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )
    arama_cubugu.send_keys("gömlek")
    arama_button = driver.find_element(By.XPATH, "//button[@class='search-button']")
    arama_button.click()
    print("Arama yapıldı: gömlek")

    # 5. Arama sonuçlarının yüklendiğini doğrula (assertion)
    sonuc_sayisi = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product-list-info"))
    )
    assert sonuc_sayisi.is_displayed(), "Arama sonuçları yüklenmedi!"
    print("Arama sonuçları başarıyla yüklendi!")

    # Biraz bekle (isteğe bağlı, sonucu gözlemlemek için)
    time.sleep(2)

except Exception as e:
    print(f"Bir hata oluştu: {e}")
    raise  # Hata detayını Jenkins konsolunda görmek için

finally:
    # Tarayıcıyı kapat
    driver.quit()
    print("Tarayıcı kapatıldı.")
