import os
import random
from PIL import Image, ImageDraw

# --- НАСТРОЙКИ ---
TEXTURE_FILE = "bill.png"  # Имя твоего файла с текстурой
BILL_WIDTH = 150           # Ширина купюры на графике (в пикселях)
BILL_HEIGHT = 20           # Высота одной купюры (толщина)
VERTICAL_STEP = 12         # Насколько плотно лежат купюры (меньше высоты = перекрытие)
# -----------------

def get_banknote_image():
    """
    Пытается загрузить картинку. Если её нет — рисует 'заглушку'.
    """
    if os.path.exists(TEXTURE_FILE):
        try:
            img = Image.open(TEXTURE_FILE).convert("RGBA")
            # Масштабируем картинку под наши настройки, чтобы все было ровно
            img = img.resize((BILL_WIDTH, BILL_HEIGHT))
            return img
        except Exception as e:
            print(f"Ошибка при чтении картинки: {e}")
    
    print("Текстура не найдена! Рисую запасной вариант...")
    # ЗАПАСНОЙ ВАРИАНТ (если ты забыл положить bill.png)
    img = Image.new('RGBA', (BILL_WIDTH, BILL_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, BILL_WIDTH, BILL_HEIGHT], fill=(50, 100, 50), outline=(30, 60, 30))
    draw.line([5, 5, BILL_WIDTH-5, 5], fill=(100, 150, 100), width=2)
    return img

def generate_realistic_chart(numbers, output_filename="result.png"):
    banknote = get_banknote_image()
    b_w, b_h = banknote.size
    
    max_bills = max(numbers) if numbers else 0
    num_stacks = len(numbers)
    
    # Считаем размер холста
    canvas_width = num_stacks * (b_w + 60) + 60
    # Высота: кол-во купюр * шаг + место под текст
    canvas_height = (max_bills * VERTICAL_STEP) + b_h + 100
    
    # Прозрачный или белый фон
    bg_color = (255, 255, 255, 255) # Белый
    canvas = Image.new('RGBA', (canvas_width, canvas_height), bg_color)
    draw = ImageDraw.Draw(canvas)
    
    current_x = 60
    
    for count in numbers:
        # Координата Y для самой нижней купюры
        base_y = canvas_height - 60
        
        # Подпись числа
        text = str(count)
        # Примерное центрирование текста (упрощено, т.к. без загрузки шрифтов ширина неизвестна)
        draw.text((current_x + b_w//2 - 5, base_y + 20), text, fill="black")
        
        for i in range(count):
            # Считаем координату Y (снизу вверх)
            y = base_y - (i * VERTICAL_STEP)
            
            # Рандомизация:
            # 1. Сдвиг влево-вправо (чтобы стопка была не идеальной)
            offset_x = random.randint(-2, 2)
            
            # 2. Небольшой поворот (опционально, требует качественной картинки с прозрачными краями)
            # Если края картинки обрезаны жестко, поворот лучше убрать
            # rotated_bill = banknote.rotate(random.randint(-1, 1), expand=True)
            
            # Вставляем купюру
            # paste работает так: (картинка, координаты, маска прозрачности)
            canvas.paste(banknote, (current_x + offset_x, y), banknote)
            
            # Затемнение нижних купюр (для объема)
            # Это продвинутая техника: рисуем полупрозрачный черный слой поверх нижних
            if i < count - 1:
                shadow = Image.new('RGBA', (b_w, b_h), (0, 0, 0, int(30 * (1 - i/count))))
                # canvas.paste(shadow, (current_x + offset_x, y), shadow) # Раскомментируй для теней

        current_x += b_w + 60

    canvas.save(output_filename)
    print(f"Готово! Сохранено в {output_filename}")

if __name__ == "__main__":
    user_input = input("Введи числа (например 10 50 20): ")
    try:
        data = [int(x) for x in user_input.split()]
        generate_realistic_chart(data)
    except ValueError:
        print("Нужны только числа!")
