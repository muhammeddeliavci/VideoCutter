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

## Kurulum

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

## Kullanım

1. Programı çalıştırın:
   ```
   python video_cutter.py
   ```

2. "Dosya Seç" butonuna tıklayın ve parçalamak istediğiniz videoyu seçin.
3. Parça süresini (dakika cinsinden) belirleyin.
4. Video kalitesini seçin.
5. "Parçalara Böl" butonuna tıklayın.
6. Parçaların kaydedileceği klasörü seçin.
7. Program videoyu parçalara bölecek ve işlem tamamlandığında bildirim verecektir.

## Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır. 