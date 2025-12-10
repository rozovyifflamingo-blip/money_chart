import os
import glob
import random
from PIL import Image, ImageDraw

# --- НОВЫЕ НАСТРОЙКИ ПОД ТВОЕ ФОТО ---
SEARCH_PATTERN = "bill.*" 

# Мы НЕ сжимаем картинку до 5px, иначе будет серая каша.
# Мы оставляем её достаточно крупной, чтобы была видна текстура.
BILL_WIDTH = 130           
BILL_HEIGHT = 25           # Высота картинки (достаточная для деталей)

# Но шаг делаем МАЛЕНЬКИМ. 
# Это значит, что каждая следующая купюра перекроет 80% предыдущей.
# Останется виден только "краешек" в 5 пикселей.
VERTICAL_STEP = 5          
# ------------------------------

def find_and_load_texture():
    all_files = os.listdir('.')
    found_files = glob.glob(SEARCH_PATTERN)
    
    if not found_files:
        # Ищем без учета регистра
        found_files = [f for f in all_files if f.lower().startswith('bill.')]

    if not found_files:
        print("❌ ОШИБКА: Файл 'bill.png' не найден!")
        return None

    texture_path = found_files[0]
    print(f"✅ Текстура найдена: {texture_path}")

    try:
        img = Image.open(texture_path).convert("RGBA")
        # Масштабируем до наших размеров
        img = img.resize((BILL_WIDTH, BILL_HEIGHT))
        return img
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        return None

def generate_chart(numbers, output_filename="result.png"):
    banknote = find_and_load_texture()
    
    if banknote is None:
        print("Стоп. Нет картинки - нет графика.")
        return

    b_w, b_h = banknote.size
    max_bills = max(numbers) if numbers else 0
    num_stacks = len(numbers)
    
    # Расчет холста
    canvas_width = num_stacks * (b_w + 50) + 50
    canvas_height = (max_bills * VERTICAL_STEP) + b_h + 80
    
    # Белый фон
    canvas = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    current_x = 50
    
    for count in numbers:
        base_y = canvas_height - 50
        
        # Подпись
        draw.text((current_x + b_w//2 - 10, base_y + 10), str(count), fill="black")
        
        for i in range(count):
            # Координата Y
            y = base_y - (i * VERTICAL_STEP)
            
            # Легкий "джиттер" (сдвиг), чтобы стопка не была идеальной
            offset_x = random.randint(-1, 1)
            
            # Рисуем купюру
            canvas.paste(banknote, (current_x + offset_x, y), mask=banknote)
            
            # ТЕНЬ НЕ НУЖНА, так как у твоего фото есть свои тени и детали.
            # Если включить программную тень, картинка станет грязной.
            
        current_x += b_w + 50

    canvas.save(output_filename)
    print(f"🎉 Готово! Файл: {output_filename}")

if __name__ == "__main__":
    user_input = input("Введи числа (например: 10 30 15): ")
    try:
        data = [int(x) for x in user_input.split()]
        generate_chart(data)
    except ValueError:
        print("Только числа!")
