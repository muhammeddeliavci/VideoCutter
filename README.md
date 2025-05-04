# Video Parçalayıcı

Video dosyalarını belirlenen sürelerde (dakika cinsinden) parçalara bölen, kullanımı kolay bir masaüstü uygulaması.

## Özellikler

- Video dosyalarını istediğiniz dakika uzunluğunda parçalara böler
- Sezgisel ve kullanıcı dostu grafiksel arayüz
- Video kalitesi seçimi (Düşük, Orta, Yüksek)
- İlerleme durumu ve tahmini kalan süre gösterimi
- İşlemi iptal etme özelliği
- Detaylı durum bildirimleri
- Video bilgilerini (süre, boyut) görüntüleme

## Gereksinimler

- Python 3.6 veya üzeri
- FFmpeg (PATH üzerinde erişilebilir olmalı)
- MoviePy kütüphanesi
- tkinter (genellikle Python ile birlikte gelir)

## Kurulum Seçenekleri

### A) Python Kurulumu ile Kullanım

1. Bu depoyu klonlayın:
   ```
   git clone https://github.com/kullanıcıadı/VideoCutter.git
   cd VideoCutter
   ```

2. Sanal ortam oluşturun ve etkinleştirin:
   ```
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. Gerekli paketleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

4. FFmpeg'i yükleyin:
   - Windows: https://ffmpeg.org/download.html adresinden indirin ve PATH'e ekleyin
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`

5. Programı çalıştırın:
   ```
   python video_cutter.py
   ```

### B) Tek Dosyalı EXE Oluşturma

Uygulamayı Python olmayan sistemlerde de çalıştırmak için EXE dosyası oluşturabilirsiniz:

1. PyInstaller ve diğer gerekli paketleri yükleyin:
   ```
   pip install -r requirements.txt
   pip install pyinstaller pillow
   ```

2. İkon oluşturun (isteğe bağlı):
   ```
   python icon_creator.py
   ```

3. EXE dosyasını oluşturun:
   ```
   python build_exe.py
   ```

4. Oluşturulan EXE dosyası `dist` klasöründe bulunacaktır.

### C) Windows Kurulum Dosyası Oluşturma

Tam bir Windows kurulum programı oluşturmak için:

1. NSIS kurulum sistemini yükleyin:
   - https://nsis.sourceforge.io/Download adresinden indirip kurun
   - NSIS'in sistem PATH değişkenine eklendiğinden emin olun

2. Tüm yapı sürecini otomatik olarak başlatın:
   ```
   python build_all.py
   ```

3. Tüm adımlar başarıyla tamamlandığında, proje klasöründe `VideoParçalayıcı_Kurulum.exe` dosyası oluşturulacaktır.

## Kullanım

1. Programı çalıştırın.
2. "Dosya Seç" butonuna tıklayın ve parçalamak istediğiniz videoyu seçin.
3. Parça süresini (dakika cinsinden) belirleyin (varsayılan: 1 dakika).
4. Video kalitesini seçin (Düşük, Orta, Yüksek).
5. "Parçalara Böl" butonuna tıklayın.
6. Parçaların kaydedileceği klasörü seçin.
7. Uygulama, videoyu belirlenen parça süresine göre bölerek, seçilen klasöre kaydedecektir.
8. İşlem sırasında ilerleme durumu, tahmini kalan süre ve işlenen parça bilgisi gösterilir.
9. İşlemi istediğiniz zaman "İptal Et" butonuyla durdurabilirsiniz.

## Sorun Giderme

1. **"FFmpeg bulunamadı" hatası alıyorsanız:**
   - FFmpeg'i yükleyin ve PATH'e eklendiğinden emin olun
   - Windows için kurulum dosyası, FFmpeg kurulumu hakkında bilgiler içeren bir metin dosyası oluşturur

2. **Video işlenirken hata alıyorsanız:**
   - Video dosyasının sağlam olduğundan emin olun
   - Farklı bir kalite ayarı deneyin
   - Yeterli disk alanınız olduğundan emin olun

## Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır. 