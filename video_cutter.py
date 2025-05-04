import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import VideoFileClip
from moviepy.config import change_settings
import datetime
import re
import subprocess
import tempfile
import threading
import time

# FFmpeg yapılandırması
change_settings({"FFMPEG_BINARY": "ffmpeg", "IMAGEMAGICK_BINARY": "convert"})

class VideoCutter:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Parçalayıcı")
        self.root.geometry("550x450")  # Biraz daha fazla alan
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Varsayılan ikon yerine özel simge ayarla
        try:
            self.root.iconbitmap(default=self.resource_path("icon.ico"))
        except:
            pass  # İkon bulunamadıysa varsayılan simgeyi kullan
        
        # Stil ayarları
        self.style = ttk.Style()
        self.style.theme_use('vista' if os.name == 'nt' else 'clam')
        self.style.configure("TButton", font=("Arial", 10), padding=5)
        self.style.configure("TLabel", font=("Arial", 10))
        self.root.configure(bg="#f5f5f5")
        
        # Ana çerçeve
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlık
        title_label = ttk.Label(main_frame, text="Video Parçalayıcı", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Video bilgi çerçevesi
        self.info_frame = ttk.LabelFrame(main_frame, text="Video Bilgisi")
        self.info_frame.pack(fill=tk.X, pady=10)
        
        # Video seçim çerçevesi
        file_frame = ttk.Frame(self.info_frame, padding=5)
        file_frame.pack(fill=tk.X)
        
        ttk.Label(file_frame, text="Video Dosyası:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.file_label = ttk.Label(file_frame, text="Henüz seçilmedi", width=40)
        self.file_label.grid(row=0, column=1, sticky=tk.W)
        
        self.select_button = ttk.Button(file_frame, text="Dosya Seç", command=self.select_video)
        self.select_button.grid(row=0, column=2, padx=(5, 0))
        
        # Video süresi ve ek bilgiler
        self.video_info_frame = ttk.Frame(self.info_frame, padding=5)
        self.video_info_frame.pack(fill=tk.X)
        
        ttk.Label(self.video_info_frame, text="Video Süresi:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.duration_label = ttk.Label(self.video_info_frame, text="-")
        self.duration_label.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(self.video_info_frame, text="Boyut:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.size_label = ttk.Label(self.video_info_frame, text="-")
        self.size_label.grid(row=1, column=1, sticky=tk.W)
        
        # Ayarlar çerçevesi
        settings_frame = ttk.LabelFrame(main_frame, text="Parçalama Ayarları")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Parça süresi
        duration_frame = ttk.Frame(settings_frame, padding=5)
        duration_frame.pack(fill=tk.X)
        
        ttk.Label(duration_frame, text="Parça Süresi (dakika):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        # Değer doğrulama fonksiyonu
        vcmd = (self.root.register(self.validate_integer), '%P')
        self.duration_var = tk.StringVar(value="1")
        self.duration_entry = ttk.Spinbox(duration_frame, 
                                    textvariable=self.duration_var,
                                    from_=1, to=60, increment=1,
                                    width=5, 
                                    validate="key", validatecommand=vcmd)
        self.duration_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Kalite ayarı
        ttk.Label(duration_frame, text="Video Kalitesi:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(10, 0))
        self.quality_var = tk.StringVar(value="Orta")
        quality_combo = ttk.Combobox(duration_frame, textvariable=self.quality_var, width=10, state="readonly")
        quality_combo['values'] = ('Düşük', 'Orta', 'Yüksek')
        quality_combo.grid(row=1, column=1, sticky=tk.W, pady=(10, 0))
        
        # Parçalama butonu
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        self.cut_button = ttk.Button(buttons_frame, text="Parçalara Böl", 
                                     command=self.start_cutting_thread,
                                     state=tk.DISABLED)
        self.cut_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(buttons_frame, text="İptal Et", 
                                       command=self.cancel_operation,
                                       state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Durum göstergesi
        status_frame = ttk.LabelFrame(main_frame, text="İşlem Durumu")
        status_frame.pack(fill=tk.X, pady=10)
        
        # Durum etiketi
        self.status_label = ttk.Label(status_frame, text="Hazır", anchor=tk.W, padding=(5, 5))
        self.status_label.pack(side=tk.TOP, fill=tk.X)
        
        # İlerleme bilgisi çerçevesi
        progress_info_frame = ttk.Frame(status_frame, padding=5)
        progress_info_frame.pack(fill=tk.X)
        
        # İşlem yüzdesi ve kalan süre
        ttk.Label(progress_info_frame, text="İlerleme:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.percentage_label = ttk.Label(progress_info_frame, text="%0")
        self.percentage_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        
        ttk.Label(progress_info_frame, text="İşlenen Parça:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.part_label = ttk.Label(progress_info_frame, text="0/0")
        self.part_label.grid(row=0, column=3, sticky=tk.W)
        
        ttk.Label(progress_info_frame, text="Tahmini Kalan:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.time_label = ttk.Label(progress_info_frame, text="-")
        self.time_label.grid(row=1, column=1, sticky=tk.W, columnspan=3)
        
        # İlerleme çubuğu
        self.progress = ttk.Progressbar(status_frame, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(side=tk.TOP, fill=tk.X, pady=(5, 5), padx=5)
        
        # Durum değişkenleri
        self.video_path = None
        self.cancel_flag = False
        self.processing_thread = None
        self.start_time = None
        self.processing_times = []
        
    def resource_path(self, relative_path):
        """Kaynak dosyaların yolunu çöz"""
        try:
            # PyInstaller ile paketleme için
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def on_closing(self):
        """Uygulama kapatılırken kaynakları temizle"""
        if self.processing_thread and self.processing_thread.is_alive():
            if messagebox.askyesno("İşlem Devam Ediyor", 
                                   "İşlem devam ediyor. Çıkmak istediğinizden emin misiniz?"):
                self.cancel_flag = True
                self.root.destroy()
        else:
            self.root.destroy()
    
    def validate_integer(self, new_value):
        """Giriş alanının sadece pozitif tam sayı olmasını sağlar"""
        if new_value == "":
            return True
        try:
            value = int(new_value)
            return value > 0
        except ValueError:
            return False
    
    def get_file_size_str(self, file_path):
        """Dosya boyutunu insan tarafından okunabilir formatta döndürür"""
        size_bytes = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
        
    def select_video(self):
        file_path = filedialog.askopenfilename(
            title="Video Dosyası Seçin",
            filetypes=(("Video Dosyaları", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv"), ("Tüm Dosyalar", "*.*"))
        )
        
        if file_path:
            self.video_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.cut_button.config(state=tk.NORMAL)
            self.status_label.config(text="Video seçildi. Video bilgileri alınıyor...")
            self.root.update()
            
            try:
                # Video bilgilerini yükle
                video = VideoFileClip(self.video_path)
                duration_str = self.format_time(video.duration)
                self.duration_label.config(text=duration_str)
                
                # Dosya boyutu
                size_str = self.get_file_size_str(self.video_path)
                self.size_label.config(text=size_str)
                
                video.close()
                
                self.status_label.config(text="Video seçildi. Parçalamak için 'Parçalara Böl' butonuna tıklayın.")
            except Exception as e:
                self.status_label.config(text=f"Video bilgileri alınırken hata: {str(e)}")
                messagebox.showerror("Hata", f"Video bilgileri alınırken hata oluştu:\n{str(e)}")
    
    def format_time(self, seconds):
        """Saniye cinsinden süreyi biçimlendirilmiş süre olarak döndürür"""
        return str(datetime.timedelta(seconds=int(seconds)))
    
    def update_progress_ui(self, current, total, part_time=None):
        """İlerleme durumunu ve tahmini kalan süreyi günceller"""
        if current <= 0 or total <= 0:
            return
            
        # İlerleme yüzdesi
        percent = int((current / total) * 100)
        self.percentage_label.config(text=f"%{percent}")
        
        # Parça bilgisi
        self.part_label.config(text=f"{current}/{total}")
        
        # İlerleme çubuğunu güncelle
        self.progress.config(value=current, maximum=total)
        
        # İşlem hızını ve kalan süreyi hesapla
        if part_time is not None:
            self.processing_times.append(part_time)
            
            # Son birkaç parçanın ortalamasını al (daha doğru tahmin için)
            recent_times = self.processing_times[-min(5, len(self.processing_times)):]
            avg_time_per_part = sum(recent_times) / len(recent_times)
            
            # Kalan süreyi hesapla
            remaining_parts = total - current
            remaining_time = avg_time_per_part * remaining_parts
            
            # Kalan süreyi biçimlendir
            if remaining_time > 0:
                remaining_str = self.format_time(remaining_time)
                self.time_label.config(text=f"{remaining_str} (Ortalama: {avg_time_per_part:.1f} sn/parça)")
            else:
                self.time_label.config(text="Tamamlanıyor...")
        
        # UI'yı zorla güncelle
        self.root.update_idletasks()
    
    def cancel_operation(self):
        """İşlemi iptal et"""
        if self.processing_thread and self.processing_thread.is_alive():
            self.cancel_flag = True
            self.status_label.config(text="İşlem iptal ediliyor...")
            self.cut_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.DISABLED)
            
            # UI'yı hızlıca güncelle
            self.root.update_idletasks()
    
    def start_cutting_thread(self):
        """Video kesme işlemini ayrı bir iş parçacığında başlat"""
        self.cancel_flag = False
        self.cut_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        
        # İlerleme göstergelerini sıfırla
        self.percentage_label.config(text="%0")
        self.part_label.config(text="0/0")
        self.time_label.config(text="-")
        self.progress.config(value=0)
        self.processing_times = []
        
        # İşlem başlangıç zamanını kaydet
        self.start_time = time.time()
        
        # İşlemi başlat
        self.processing_thread = threading.Thread(target=self.cut_video)
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def cut_video(self):
        """Video kesme işlemini gerçekleştir"""
        if not self.video_path:
            messagebox.showerror("Hata", "Lütfen önce bir video dosyası seçin.")
            return
        
        try:
            part_duration_min = int(self.duration_var.get())
            if part_duration_min <= 0:
                raise ValueError("Parça süresi pozitif bir sayı olmalıdır.")
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir parça süresi giriniz.")
            return
            
        # Çıktı klasörünü seç
        output_dir = filedialog.askdirectory(title="Parçaların Kaydedileceği Klasörü Seçin")
        if not output_dir:
            self.cut_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)
            return
        
        # Kalite ayarını belirle
        quality_settings = {
            "Düşük": {"crf": "28", "preset": "faster"},
            "Orta": {"crf": "23", "preset": "medium"},
            "Yüksek": {"crf": "18", "preset": "slow"}
        }
        selected_quality = self.quality_var.get()
        quality = quality_settings.get(selected_quality, quality_settings["Orta"])
        
        try:
            self.status_label.config(text="FFmpeg kontrol ediliyor...")
            self.root.update()
            
            # FFmpeg mevcut mu kontrol et
            try:
                process = subprocess.run(['ffmpeg', '-version'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               check=True)
                if process.returncode != 0:
                    raise Exception("FFmpeg sürümü alınamadı")
                
                # FFmpeg sürümünü göster
                ffmpeg_version = process.stdout.decode('utf-8', errors='ignore').split('\n')[0]
                self.status_label.config(text=f"FFmpeg bulundu: {ffmpeg_version}")
                self.root.update()
                
            except (subprocess.SubprocessError, FileNotFoundError) as e:
                messagebox.showerror("Hata", f"FFmpeg bulunamadı veya çalıştırılamadı: {str(e)}\nLütfen FFmpeg'i yükleyin ve PATH değişkenine ekleyin.")
                self.cut_button.config(state=tk.NORMAL)
                self.cancel_button.config(state=tk.DISABLED)
                return
            
            # Video yükleme
            self.status_label.config(text="Video yükleniyor... Lütfen bekleyin.")
            self.root.update()
            
            video = VideoFileClip(self.video_path)
            video_duration = video.duration
            
            # Parça süresi (saniye cinsinden)
            part_duration = part_duration_min * 60  # Dakikayı saniyeye çevir
            
            # Parça sayısı hesaplama
            num_parts = int(video_duration // part_duration)
            if video_duration % part_duration > 0:
                num_parts += 1
            
            # Dosya adı hazırlama
            base_filename = os.path.splitext(os.path.basename(self.video_path))[0]
            # Dosya adından özel karakterleri temizle
            base_filename = re.sub(r'[^\w\s-]', '', base_filename)
            base_filename = re.sub(r'[-\s]+', '_', base_filename)
            
            # İlerleme çubuğunu göster ve yapılandır
            self.update_progress_ui(0, num_parts)
            
            successful_parts = 0
            total_start_time = time.time()
            
            # Her parçayı oluşturma
            for i in range(num_parts):
                if self.cancel_flag:
                    self.status_label.config(text="İşlem iptal edildi.")
                    break
                    
                part_start_time = time.time()
                start_time = i * part_duration
                end_time = min((i + 1) * part_duration, video_duration)
                
                current_duration = end_time - start_time
                percent_of_video = (current_duration / video_duration) * 100
                
                self.status_label.config(text=f"Parça {i+1}/{num_parts} işleniyor... ({self.format_time(start_time)} - {self.format_time(end_time)})")
                self.update_progress_ui(i, num_parts)
                
                # Geçici dosya kullan - FFmpeg'in stdout hatalarını önlemek için
                with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                    temp_path = temp_file.name
                
                try:
                    # Parçayı kaydetme
                    start_time_str = self.format_time(start_time).replace(":", "-")
                    end_time_str = self.format_time(end_time).replace(":", "-")
                    output_filename = f"{base_filename}_part{i+1}_{start_time_str}_{end_time_str}.mp4"
                    output_path = os.path.join(output_dir, output_filename)
                    
                    # FFmpeg'i doğrudan komut olarak çalıştır (daha güvenilir)
                    command = [
                        "ffmpeg", "-y",
                        "-i", self.video_path,
                        "-ss", str(start_time),
                        "-to", str(end_time),
                        "-c:v", "libx264",
                        "-c:a", "aac",
                        "-crf", quality["crf"],
                        "-preset", quality["preset"],
                        output_path
                    ]
                    
                    try:
                        self.status_label.config(text=f"Parça {i+1}/{num_parts} işleniyor... FFmpeg ile video oluşturuluyor")
                        self.root.update_idletasks()
                        
                        process = subprocess.run(
                            command, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE
                        )
                        
                        if process.returncode != 0:
                            error_msg = process.stderr.decode('utf-8', errors='ignore')
                            raise Exception(f"FFmpeg işlemi başarısız: {error_msg}")
                        
                        successful_parts += 1
                            
                    except Exception as e:
                        # Alternatif yöntem: MoviePy kullan
                        self.status_label.config(text=f"FFmpeg ile hata, alternatif yöntem deneniyor...")
                        self.root.update_idletasks()
                        
                        # Videoyu kesme
                        part = video.subclip(start_time, end_time)
                        
                        part.write_videofile(
                            temp_path,  # Önce geçici dosyaya yaz
                            codec="libx264", 
                            audio_codec="aac",
                            temp_audiofile=None,
                            remove_temp=True,
                            threads=2,
                            logger=None,  # stdout hatası için logger None olarak ayarla
                            verbose=False,
                            ffmpeg_params=["-crf", quality["crf"]]
                        )
                        
                        # Geçici dosyayı hedef konuma taşı
                        if os.path.exists(temp_path):
                            if os.path.exists(output_path):
                                os.remove(output_path)
                            os.rename(temp_path, output_path)
                            successful_parts += 1
                            
                except Exception as write_err:
                    if not self.cancel_flag:
                        self.status_label.config(text=f"Parça {i+1} kaydedilirken hata: {str(write_err)}")
                        messagebox.showerror("Hata", f"Parça {i+1} kaydedilirken hata oluştu:\n{str(write_err)}")
                finally:
                    # Geçici dosyayı temizle
                    if os.path.exists(temp_path):
                        try:
                            os.remove(temp_path)
                        except:
                            pass
                    
                    # Parça işleme süresini hesapla
                    part_process_time = time.time() - part_start_time
                    
                    # İlerleme ve kalan süre tahmini güncelle
                    self.update_progress_ui(i + 1, num_parts, part_process_time)
                    
                    # Kullanıcıya durum güncellemesi
                    elapsed = time.time() - total_start_time
                    elapsed_str = self.format_time(elapsed)
                    
                    # Durum güncelle
                    if i < num_parts - 1 and not self.cancel_flag:
                        self.status_label.config(
                            text=f"Parça {i+1}/{num_parts} tamamlandı ({elapsed_str} geçti). Bir sonraki parça hazırlanıyor..."
                        )
            
            if hasattr(video, 'close'):
                video.close()
            
            # Toplam işlem süresini hesapla
            total_time = time.time() - total_start_time
            total_time_str = self.format_time(total_time)
            
            # İlerleme çubuğunu güncelle ve tamamlandı mesajını göster
            if self.cancel_flag:
                self.status_label.config(text=f"İşlem iptal edildi. {successful_parts}/{num_parts} parça oluşturuldu. Toplam süre: {total_time_str}")
                if successful_parts > 0:
                    messagebox.showinfo("İptal Edildi", f"İşlem iptal edildi. {successful_parts}/{num_parts} parça oluşturuldu.\nToplam işlem süresi: {total_time_str}")
            else:
                self.progress.config(value=num_parts)
                self.percentage_label.config(text="%100")
                self.status_label.config(text=f"Tamamlandı! {successful_parts}/{num_parts} parça oluşturuldu. Toplam süre: {total_time_str}")
                messagebox.showinfo("Başarılı", f"Video {successful_parts} parçaya bölündü ve kaydedildi.\nToplam işlem süresi: {total_time_str}")
            
        except Exception as e:
            self.status_label.config(text=f"Hata: {str(e)}")
            messagebox.showerror("Hata", f"Video parçalanırken bir hata oluştu:\n{str(e)}")
        finally:
            # İşlem bittikten sonra butonları sıfırla
            self.cut_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)

def main():
    """Uygulama giriş noktası"""
    root = tk.Tk()
    app = VideoCutter(root)
    root.mainloop()
    return 0

if __name__ == "__main__":
    main() 