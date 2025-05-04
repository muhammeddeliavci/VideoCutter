# FFmpeg Kurulum Betiği
$tempFile = "$env:TEMP\ffmpeg.7z"
$ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.7z"
$ffmpegDirectory = "C:\ffmpeg"

# Eğer klasör varsa temizle, yoksa oluştur
if (Test-Path -Path $ffmpegDirectory) {
    Write-Host "Mevcut FFmpeg klasörü temizleniyor..."
    Remove-Item -Path $ffmpegDirectory -Recurse -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Force -Path $ffmpegDirectory | Out-Null

# FFmpeg indirme
Write-Host "FFmpeg indiriliyor... Bu işlem biraz zaman alabilir."
Invoke-WebRequest -Uri $ffmpegUrl -OutFile $tempFile

# 7-Zip kontrol ve çıkarma
if (-not (Test-Path "C:\Program Files\7-Zip\7z.exe")) {
    Write-Host "7-Zip bulunamadı, indiriliyor ve kuruluyor..."
    $7zipUrl = "https://www.7-zip.org/a/7z2401-x64.exe"
    $7zipInstaller = "$env:TEMP\7zInstaller.exe"
    Invoke-WebRequest -Uri $7zipUrl -OutFile $7zipInstaller
    Start-Process -FilePath $7zipInstaller -Args "/S" -Wait
}

# FFmpeg arşivini çıkarma
Write-Host "FFmpeg arşivi çıkarılıyor..."
& 'C:\Program Files\7-Zip\7z.exe' x $tempFile -o"$env:TEMP\ffmpeg_temp" -y

# Çıkarılan dosyaların yapısını keşfedelim
$tempDir = "$env:TEMP\ffmpeg_temp"
Write-Host "Çıkarılan klasör içeriği listesi:"
Get-ChildItem -Path $tempDir -Recurse | ForEach-Object {
    Write-Host $_.FullName
}

# Exe dosyalarını bulalım
Write-Host "Exe dosyaları aranıyor..."
$exeFiles = Get-ChildItem -Path $tempDir -Filter "*.exe" -Recurse
foreach ($file in $exeFiles) {
    Write-Host "Exe dosyası bulundu: $($file.FullName)"
    # Dosyayı FFmpeg klasörüne kopyala
    Copy-Item $file.FullName -Destination $ffmpegDirectory
}

# PATH değişkeni düzenleme
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not $currentPath.Contains($ffmpegDirectory)) {
    Write-Host "FFmpeg PATH değişkenine ekleniyor..."
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$ffmpegDirectory", "User")
}

# Temizlik
Write-Host "Geçici dosyalar temizleniyor..."
Remove-Item -Path $tempFile -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$env:TEMP\ffmpeg_temp" -Recurse -Force -ErrorAction SilentlyContinue

# Doğrulama
if (Test-Path "$ffmpegDirectory\ffmpeg.exe") {
    Write-Host "FFmpeg kurulumu tamamlandı. C:\ffmpeg klasörüne kuruldu."
    Write-Host "Değişikliklerin etkili olması için komut istemcisini yeniden başlatın."
} else {
    Write-Host "FFmpeg kurulumunda sorun oluştu. Exe dosyaları bulunamadı."
} 