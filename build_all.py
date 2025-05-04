eimport os
import sys
import subprocess
import time

def display_header():
    print("\n" + "=" * 70)
    print("          Video Parçalayıcı - Tüm Dosyaları Oluşturma Aracı")
    print("=" * 70)
    print("Bu program, şu işlemleri gerçekleştirecek:")
    print("1. Gerekli kütüphaneleri kontrol edip kurma")
    print("2. Uygulama için ikon oluşturma")
    print("3. EXE dosyası oluşturma")
    print("4. Windows kurulum dosyası oluşturma (NSIS gerektirir)")
    print("=" * 70)

def check_and_install_requirements():
    print("\n[1/4] Gerekli kütüphaneleri kontrol edip kurma...")
    
    # Gerekli kütüphaneler
    requirements = [
        "moviepy",
        "pyinstaller",
        "pillow"
    ]
    
    for package in requirements:
        print(f"  {package} kontrol ediliyor...", end="")
        try:
            __import__(package.replace("-", "_"))
            print(" [TAMAM]")
        except ImportError:
            print(" [YOK] - Yükleniyor...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("  Tüm kütüphaneler hazır.")

def create_icon():
    print("\n[2/4] Uygulama için ikon oluşturma...")
    if os.path.exists("icon.ico"):
        user_input = input("  İkon dosyası zaten mevcut. Yeniden oluşturmak ister misiniz? (e/h): ")
        if user_input.lower() != 'e':
            print("  Mevcut ikon kullanılacak.")
            return
    
    try:
        import icon_creator
        icon_creator.create_icon()
        print("  İkon oluşturuldu: icon.ico")
    except Exception as e:
        print(f"  İkon oluşturulurken hata: {str(e)}")
        print("  Varsayılan ikon kullanılacak.")

def build_exe():
    print("\n[3/4] EXE dosyası oluşturma...")
    
    # PyInstaller'ı kontrol et
    try:
        import PyInstaller
        print(f"  PyInstaller sürümü: {PyInstaller.__version__}")
    except ImportError:
        print("  PyInstaller kurulu değil, kuruluyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # build_exe.py scriptini çalıştır
    try:
        print("  EXE oluşturma işlemi başlatılıyor...")
        import build_exe
        print("  EXE dosyası oluşturuldu: dist/VideoParçalayıcı.exe")
    except Exception as e:
        print(f"  EXE oluşturulurken hata: {str(e)}")
        return False
    
    return True

def create_installer():
    print("\n[4/4] Windows kurulum dosyası oluşturma...")
    
    # NSIS kontrol et
    nsis_cmd = "makensis"
    try:
        result = subprocess.run([nsis_cmd, "-VERSION"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("  NSIS bulundu.")
        else:
            raise Exception("NSIS çalıştırılamadı")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("  NSIS bulunamadı!")
        print("  NSIS'i şu adresten yükleyebilirsiniz: https://nsis.sourceforge.io/Download")
        print("  Kurulumdan sonra, makensis komutunun PATH'e eklendiğinden emin olun.")
        user_input = input("  Installer oluşturmadan devam etmek istiyor musunuz? (e/h): ")
        if user_input.lower() != 'e':
            return False
        return True
    
    # make_installer.py scriptini çalıştır
    try:
        print("  Kurulum dosyası oluşturma işlemi başlatılıyor...")
        import make_installer
        make_installer.create_installer()
    except Exception as e:
        print(f"  Kurulum dosyası oluşturulurken hata: {str(e)}")
        return False
    
    return True

def main():
    display_header()
    
    # Kullanıcı onayı
    user_input = input("\nDevam etmek istiyor musunuz? (e/h): ")
    if user_input.lower() != 'e':
        print("İşlem iptal edildi.")
        return
    
    # 1. Kütüphaneleri kontrol et
    check_and_install_requirements()
    
    # 2. İkon oluştur
    create_icon()
    
    # 3. EXE oluştur
    if not build_exe():
        print("\nEXE oluşturma başarısız oldu, işlem durduruluyor.")
        return
    
    # 4. Kurulum dosyası oluştur
    create_installer()
    
    print("\n" + "=" * 70)
    print("Tüm işlemler tamamlandı!")
    print("=" * 70)
    
    # Sonuç dosyalarını listele
    exe_path = os.path.abspath("dist/VideoParçalayıcı.exe")
    installer_path = os.path.abspath("VideoParçalayıcı_Kurulum.exe")
    
    print("\nOluşturulan dosyalar:")
    if os.path.exists(exe_path):
        print(f"  EXE Dosyası: {exe_path}")
    if os.path.exists(installer_path):
        print(f"  Kurulum Dosyası: {installer_path}")
    
    print("\nNOT: Video Parçalayıcı uygulaması FFmpeg'e ihtiyaç duymaktadır.")
    print("     Kurulum dosyası, FFmpeg kurulumu hakkında bilgiler içermektedir.")

if __name__ == "__main__":
    main() 