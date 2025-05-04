import os
import sys
import subprocess
import shutil
import PyInstaller.__main__

print("Video Parçalayıcı - .exe Oluşturma Programı")
print("===========================================")

# PyInstaller'ın kurulu olup olmadığını kontrol et
try:
    import PyInstaller
    print("PyInstaller sürümü:", PyInstaller.__version__)
except ImportError:
    print("PyInstaller kurulu değil. Kuruluyor...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("PyInstaller kuruldu.")

# dist ve build klasörlerini temizle
if os.path.exists("dist"):
    print("Önceki dist klasörü temizleniyor...")
    shutil.rmtree("dist")
if os.path.exists("build"):
    print("Önceki build klasörü temizleniyor...")
    shutil.rmtree("build")
if os.path.exists("video_cutter.spec"):
    print("Önceki spec dosyası siliniyor...")
    os.remove("video_cutter.spec")

print("\nPyInstaller ile .exe dosyası oluşturuluyor...")

# İkon dosyası var mı kontrol et
icon_path = None
if os.path.exists("icon.ico"):
    icon_path = "icon.ico"
    print("İkon bulundu:", icon_path)
else:
    print("İkon bulunamadı, varsayılan ikon kullanılacak.")

# PyInstaller argümanlarını oluştur
pyinstaller_args = [
    "video_cutter.py",  # Ana Python dosyası
    "--onefile",        # Tek dosyalı .exe oluştur
    "--windowed",       # Konsol penceresi gösterme
    "--noconfirm",      # Onay sorma
    "--clean",          # Temiz derleme
    "--name=VideoParçalayıcı"  # Çıktı dosyasının adı
]

# İkon varsa ekle
if icon_path:
    pyinstaller_args.append(f"--icon={icon_path}")

# PyInstaller'ı çalıştır
PyInstaller.__main__.run(pyinstaller_args)

print("\n.exe dosyası oluşturma işlemi tamamlandı!")
print("Oluşturulan .exe dosyası: dist/VideoParçalayıcı.exe")
print("\nKullanım: VideoParçalayıcı.exe dosyasını çift tıklatarak çalıştırabilirsiniz.")
print("NOT: Program çalışmak için FFmpeg'e ihtiyaç duyar. FFmpeg'in sisteminizde kurulu olduğundan emin olun.") 