from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    print("Video Parçalayıcı için ikon oluşturuluyor...")
    
    # Ikon boyutları
    size = 256
    
    # Yeni bir görüntü oluştur
    icon = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # Arka plan dairesi
    draw.ellipse((10, 10, size-10, size-10), fill=(33, 150, 243, 255))
    
    # Video şekli (beyaz kare)
    rect_margin = size // 5
    draw.rectangle(
        (rect_margin, rect_margin, size-rect_margin, size-rect_margin), 
        fill=(255, 255, 255, 240)
    )
    
    # Kesik çizgilerle bölünme efekti
    line_width = 6
    line_color = (33, 150, 243, 255)
    dash_length = 15
    
    # Yatay kesik çizgi
    middle_y = size // 2
    current_x = rect_margin
    while current_x < size - rect_margin:
        end_x = min(current_x + dash_length, size - rect_margin)
        draw.line([(current_x, middle_y), (end_x, middle_y)], fill=line_color, width=line_width)
        current_x = end_x + dash_length
    
    # Dikey kesik çizgi
    middle_x = size // 2
    current_y = rect_margin
    while current_y < size - rect_margin:
        end_y = min(current_y + dash_length, size - rect_margin)
        draw.line([(middle_x, current_y), (middle_x, end_y)], fill=line_color, width=line_width)
        current_y = end_y + dash_length
    
    # "VP" harflerini ekle (Opsiyonel)
    try:
        # Varsayılan bir font kullan - bulunabilirse
        font_size = size // 4
        font = ImageFont.truetype("arial.ttf", font_size)
        draw.text((size//2-font_size//2, size//2-font_size//2), "VP", fill=(0, 0, 0, 200), font=font)
    except IOError:
        # Font bulunamazsa, bu kısmı atlayabilirsiniz
        print("Font bulunamadı, VP harfleri eklenmedi.")
    
    # İkonu farklı boyutlarda kaydet
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for s in sizes:
        img = icon.resize((s, s), Image.LANCZOS)
        images.append(img)
    
    # ICO formatında kaydet
    icon_path = "icon.ico"
    images[0].save(icon_path, format="ICO", sizes=[(s, s) for s in sizes])
    
    # PNG olarak da kaydet
    png_path = "icon.png"
    icon.save(png_path, format="PNG")
    
    print(f"İkon oluşturuldu: {icon_path} ve {png_path}")
    return icon_path

if __name__ == "__main__":
    create_icon() 