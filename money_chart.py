import os
import glob
import random
from PIL import Image, ImageDraw

# --- НАСТРОЙКИ ДЛЯ РЕАЛИЗМА ---
# Ищем любой файл, начинающийся на bill (png, jpg...)
SEARCH_PATTERN = "bill.*" 

# Делаем купюру тонкой и широкой, как реальный торец пачки
BILL_WIDTH = 140           
BILL_HEIGHT = 5            # Высота 5 пикселей (сплющиваем картинку)
VERTICAL_STEP = 4          # Шаг 4 пикселя (плотная укладка)
# ------------------------------

def find_and_load_texture():
    """Ищет файл текстуры и загружает его."""
    all_files = os.listdir('.')
    # Ищем файлы по шаблону bill.*
    found_files = glob.glob(SEARCH_PATTERN)
    
    if not found_files:
        # Пробуем без учета регистра
        found_files = [f for f in all_files if f.lower().startswith('bill.')]

    if not found_files:
        print("❌ ОШИБКА: Файл 'bill.png' (или jpg) не найден!")
        return None

    texture_path = found_files[0]
    print(f"✅ Использую текстуру: {texture_path}")

    try:
        img = Image.open(texture_path).convert("RGBA")
        # Сплющиваем изображение до размера торца купюры
        img = img.resize((BILL_WIDTH, BILL_HEIGHT))
        return img
    except Exception as e:
        print(f"❌ ОШИБКА картинки: {e}")
        return None

def create_fallback_texture():
    """Рисует заглушку, если картинки нет."""
    img = Image.new('RGBA', (BILL_WIDTH, BILL_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, BILL_WIDTH, BILL_HEIGHT], fill=(85, 120, 85), outline=(50, 80, 50))
    return img

def generate_chart(numbers, output_filename="result.png"):
    banknote = find_and_load_texture()
    
    if banknote is None:
        banknote = create_fallback_texture()

    b_w, b_h = banknote.size
    max_bills = max(numbers) if numbers else 0
    num_stacks = len(numbers)
    
    # Размер холста
    canvas_width = num_stacks * (b_w + 60) + 60
    canvas_height = (max_bills * VERTICAL_STEP) + b_h + 100
    
    # Создаем фон
    canvas = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    current_x = 60
    
    # --- ГЛАВНЫЙ ЦИКЛ ---
    for count in numbers:
        base_y = canvas_height - 60
        
        # Подпись числа
        draw.text((current_x + b_w//2 - 10, base_y + 15), str(count), fill="black")
        
        for i in range(count):
            # Считаем координату Y
            y = base_y - (i * VERTICAL_STEP)
            
            # Небольшой рандом влево-вправо
            offset_x = random.randint(-1, 1)
            
            # Рисуем саму купюру
            canvas.paste(banknote, (current_x + offset_x, y), banknote)
            
            # --- ТЕНЬ (для объема) ---
            # Чем ниже купюра в стопке, тем темнее она накрывается тенью
            if i < count - 1: 
                # Рассчитываем прозрачность тени (чем ниже, тем темнее)
                # Максимальная тень = 60 из 255
                opacity = int(60 * (1 - i / count)) 
                
                if opacity > 0:
                    shadow = Image.new('RGBA', (b_w, b_h), (0, 0, 0, opacity))
                    # Накладываем тень только на форму купюры (mask=banknote)
                    canvas.paste(shadow, (current_x + offset_x, y), mask=banknote)

        current_x += b_w + 60

    canvas.save(output_filename)
    print(f"🎉 Готово! Файл сохранен как {output_filename}")

if __name__ == "__main__":
    print("Генератор денежных диаграмм запущен.")
    user_input = input("Введи числа через пробел (например: 100 50 250): ")
    try:
        data = [int(x) for x in user_input.split()]
        generate_chart(data)
    except ValueError:
        print("Ошибка: нужно вводить только числа!")
