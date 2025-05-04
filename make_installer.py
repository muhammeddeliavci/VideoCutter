import os
import subprocess
import sys
import tempfile
import shutil

# NSIS kurulum script şablonu
NSIS_TEMPLATE = r"""
!include "MUI2.nsh"
!include "FileFunc.nsh"

; Uygulama bilgileri
Name "Video Parçalayıcı"
OutFile "VideoParçalayıcı_Kurulum.exe"
Unicode True

; Varsayılan kurulum konumu
InstallDir "$PROGRAMFILES\VideoParçalayıcı"

; Registry anahtarları
!define REGKEY "Software\VideoParçalayıcı"

; Modern arayüz ayarları
!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP "installer_image.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "header_image.bmp"
!define MUI_HEADERIMAGE_RIGHT

; Arayüz sayfaları
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Kaldırma sayfaları
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Dil dosyaları
!insertmacro MUI_LANGUAGE "Turkish"

; Kurulum başlangıç fonksiyonu
Function .onInit
  ; Otomatik kapatma
  SetAutoClose true
FunctionEnd

; Kurulum bölümü
Section "Program Dosyaları" SecProgram
  SetOutPath "$INSTDIR"
  
  ; Uygulama dosyalarını kopyala
  File "dist\VideoParçalayıcı.exe"
  File "icon.ico"
  File "LICENSE"
  File "README.md"
  
  ; FFmpeg kurulumu bilgilerini içeren bir metin dosyası oluştur
  FileOpen $0 "$INSTDIR\ffmpeg_kurulum.txt" w
  FileWrite $0 "Video Parçalayıcı, FFmpeg'e ihtiyaç duyar.$\r$\n"
  FileWrite $0 "FFmpeg'i şu adreslerden indirebilirsiniz:$\r$\n"
  FileWrite $0 "https://ffmpeg.org/download.html$\r$\n"
  FileWrite $0 "https://github.com/BtbN/FFmpeg-Builds/releases$\r$\n$\r$\n"
  FileWrite $0 "FFmpeg'i indirdikten sonra, bin klasöründeki ffmpeg.exe dosyasını sistem PATH değişkeninize ekleyin.$\r$\n"
  FileClose $0
  
  ; Başlat menüsü kısayolları oluştur
  CreateDirectory "$SMPROGRAMS\Video Parçalayıcı"
  CreateShortcut "$SMPROGRAMS\Video Parçalayıcı\Video Parçalayıcı.lnk" "$INSTDIR\VideoParçalayıcı.exe" "" "$INSTDIR\icon.ico"
  CreateShortcut "$SMPROGRAMS\Video Parçalayıcı\Kaldır.lnk" "$INSTDIR\uninstall.exe"
  CreateShortcut "$SMPROGRAMS\Video Parçalayıcı\FFmpeg Kurulum Bilgisi.lnk" "$INSTDIR\ffmpeg_kurulum.txt"
  
  ; Masaüstü kısayolu oluştur
  CreateShortcut "$DESKTOP\Video Parçalayıcı.lnk" "$INSTDIR\VideoParçalayıcı.exe" "" "$INSTDIR\icon.ico"
  
  ; Registry değerleri oluştur (kaldırma için)
  WriteRegStr HKLM "${REGKEY}" "InstallDir" $INSTDIR
  WriteRegStr HKLM "${REGKEY}" "Version" "1.0.0"
  
  ; Kaldırma bilgilerini yaz
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VideoParçalayıcı" "DisplayName" "Video Parçalayıcı"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VideoParçalayıcı" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VideoParçalayıcı" "DisplayIcon" "$INSTDIR\icon.ico"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VideoParçalayıcı" "Publisher" "Video Parçalayıcı"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VideoParçalayıcı" "DisplayVersion" "1.0.0"
  
  ; Dosya boyutunu hesapla
  ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VideoParçalayıcı" "EstimatedSize" "$0"
  
  ; Kaldırma programını oluştur
  WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

; Kaldırma bölümü
Section "Uninstall"
  ; Program dosyalarını kaldır
  Delete "$INSTDIR\VideoParçalayıcı.exe"
  Delete "$INSTDIR\icon.ico"
  Delete "$INSTDIR\LICENSE"
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\ffmpeg_kurulum.txt"
  Delete "$INSTDIR\uninstall.exe"
  
  ; Klasörü sil
  RMDir "$INSTDIR"
  
  ; Başlat menüsü kısayollarını sil
  Delete "$SMPROGRAMS\Video Parçalayıcı\Video Parçalayıcı.lnk"
  Delete "$SMPROGRAMS\Video Parçalayıcı\Kaldır.lnk"
  Delete "$SMPROGRAMS\Video Parçalayıcı\FFmpeg Kurulum Bilgisi.lnk"
  RMDir "$SMPROGRAMS\Video Parçalayıcı"
  
  ; Masaüstü kısayolunu sil
  Delete "$DESKTOP\Video Parçalayıcı.lnk"
  
  ; Registry anahtar ve değerlerini sil
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\VideoParçalayıcı"
  DeleteRegKey HKLM "${REGKEY}"
SectionEnd
"""

def create_installer():
    print("Video Parçalayıcı - Kurulum Dosyası Oluşturma")
    print("=============================================")
    
    # .exe dosyasının mevcut olup olmadığını kontrol et
    if not os.path.exists("dist/VideoParçalayıcı.exe"):
        print("Hata: dist/VideoParçalayıcı.exe bulunamadı!")
        print("Lütfen önce 'python build_exe.py' komutunu çalıştırın.")
        return
    
    # İkon kontrolü
    if not os.path.exists("icon.ico"):
        print("İkon dosyası (icon.ico) bulunamadı.")
        print("İkon oluşturmak için 'python icon_creator.py' komutunu çalıştırabilirsiniz.")
        return
    
    # NSIS kontrolü
    nsis_cmd = "makensis"
    try:
        subprocess.run([nsis_cmd, "-VERSION"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("NSIS bulundu.")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("NSIS bulunamadı! Lütfen NSIS'i yükleyin: https://nsis.sourceforge.io/Download")
        print("Kurulumdan sonra, makensis komutunun PATH'e eklendiğinden emin olun.")
        return
    
    # Kurulum için gerekli görselleri oluştur
    print("Kurulum görselleri oluşturuluyor...")
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Header görüntüsü (150x57)
        header = Image.new('RGB', (150, 57), color=(255, 255, 255))
        header_draw = ImageDraw.Draw(header)
        header_draw.rectangle((0, 0, 150, 57), outline=(33, 150, 243), width=2)
        header_draw.text((10, 20), "Video Parçalayıcı", fill=(33, 150, 243))
        header.save("header_image.bmp")
        
        # Yan taraf görüntüsü (164x314)
        sidebar = Image.new('RGB', (164, 314), color=(33, 150, 243))
        sidebar_draw = ImageDraw.Draw(sidebar)
        sidebar_draw.text((10, 10), "Video\nParçalayıcı\n\nv1.0.0", fill=(255, 255, 255))
        sidebar.save("installer_image.bmp")
        
        print("Kurulum görselleri oluşturuldu.")
    except ImportError:
        print("Pillow kütüphanesi bulunamadı. Varsayılan görseller kullanılacak.")
        # Boş BMP dosyaları oluştur
        with open("header_image.bmp", "wb") as f:
            f.write(b"BM")
        with open("installer_image.bmp", "wb") as f:
            f.write(b"BM")
    
    # NSIS script dosyasını oluştur
    print("NSIS script dosyası oluşturuluyor...")
    with tempfile.NamedTemporaryFile(suffix=".nsi", delete=False) as temp:
        temp_path = temp.name
        temp.write(NSIS_TEMPLATE.encode('utf-8'))
    
    # NSIS derleyicisini çalıştır
    print("Kurulum dosyası oluşturuluyor...")
    result = subprocess.run([nsis_cmd, temp_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Geçici dosyayı temizle
    os.unlink(temp_path)
    
    if result.returncode == 0:
        print("\nKurulum dosyası başarıyla oluşturuldu: VideoParçalayıcı_Kurulum.exe")
        
        # Temp dosyalarını temizle
        if os.path.exists("header_image.bmp"):
            os.remove("header_image.bmp")
        if os.path.exists("installer_image.bmp"):
            os.remove("installer_image.bmp")
    else:
        print("Kurulum dosyası oluşturulurken bir hata oluştu:")
        print(result.stderr.decode('utf-8', errors='ignore'))

if __name__ == "__main__":
    create_installer() 