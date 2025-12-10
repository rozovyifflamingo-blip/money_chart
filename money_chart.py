import os
import glob
import random
from PIL import Image, ImageDraw

# --- НАСТРОЙКИ ---
# Мы будем искать любой файл, начинающийся на "bill" (bill.png, bill.jpg и т.д.)
SEARCH_PATTERN = "bill.*" 
BILL_WIDTH = 150
BILL_HEIGHT = 20
VERTICAL_STEP = 12
# -----------------

def find_and_load_texture():
    """
    Ищет файл текстуры и сообщает, что происходит.
    """
    # 1. Проверяем, какие файлы вообще есть в папке
    all_files = os.listdir('.')
    print(f"📂 Файлы в текущей папке: {all_files}")

    # 2. Ищем любой файл, похожий на bill.*
    found_files = glob.glob(SEARCH_PATTERN)
    
    # Если ничего не нашли, пробуем искать без учета регистра (для Bill.png)
    if not found_files:
        found_files = [f for f in all_files if f.lower().startswith('bill.')]

    if not found_files:
        print("❌ ОШИБКА: Я не нашел файл 'bill.png' (или jpg)!")
        print("   Убедись, что загрузил файл и он называется 'bill'")
        return None

    texture_path = found_files[0]
    print(f"✅ Найдена текстура: {texture_path}")

    try:
        img = Image.open(texture_path).convert("RGBA")
        img = img.resize((BILL_WIDTH, BILL_HEIGHT))
        print("✅ Текстура успешно загружена и обработана.")
        return img
    except Exception as e:
        print(f"❌ ОШИБКА при открытии картинки: {e}")
        return None

def create_fallback_texture():
    print("⚠️ Использую запасную (рисованную) текстуру.")
    img = Image.new('RGBA', (BILL_WIDTH, BILL_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, BILL_WIDTH, BILL_HEIGHT], fill=(100, 150, 100), outline=(50, 80, 50))
    draw.text((10, 2), "NO IMG", fill="white")
    return img

def generate_chart(numbers, output_filename="result.png"):
    # Пытаемся загрузить фото
    banknote = find_and_load_texture()
    
    # Если фото нет или сломано — делаем заглушку
    if banknote is None:
        banknote = create_fallback_texture()

    b_w, b_h = banknote.size
    max_bills = max(numbers) if numbers else 0
    num_stacks = len(numbers)
    
    canvas_width = num_stacks * (b_w + 60) + 60
    canvas_height = (max_bills * VERTICAL_STEP) + b_h + 100
    
    canvas = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    current_x = 60
    for count in numbers:
        base_y = canvas_height - 60
        draw.text((current_x + b_w//2 - 5, base_y + 20), str(count), fill="black")
        
        for i in range(count):
            y = base_y - (i * VERTICAL_STEP)
            offset_x = random.randint(-2, 2)
            canvas.paste(banknote, (current_x + offset_x, y), banknote)
            
            # Тень для реализма
            if i < count - 1:
                shadow = Image.new('RGBA', (b_w, b_h), (0, 0, 0, int(40 * (1 - i/count))))
                # canvas.paste(shadow, (current_x + offset_x, y), shadow)

        current_x += b_w + 60

    canvas.save(output_filename)
    print(f"🎉 Готово! Результат сохранен в {output_filename}")

if __name__ == "__main__":
    user_input = input("Введи числа (например 10 50 20): ")
    try:
        data = [int(x) for x in user_input.split()]
        generate_chart(data)
    except ValueError:
        print("Вводи только числа!")
