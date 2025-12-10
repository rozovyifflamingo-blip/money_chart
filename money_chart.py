import random
from PIL import Image, ImageDraw, ImageFont

def create_banknote_asset():
    """
    Создает маленькое изображение одной купюры (вид сбоку/с торца).
    Генерируем его кодом, чтобы не зависеть от внешних файлов.
    """
    width = 120
    height = 15
    # Цвет купюры (зеленоватый)
    color = (133, 187, 101)
    border_color = (80, 120, 60)
    
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Рисуем прямоугольник (тело купюры)
    draw.rectangle([0, 0, width-1, height-1], fill=color, outline=border_color)
    
    # Добавляем немного "шума" или деталей, чтобы было похоже на текстуру бумаги
    draw.line([10, 7, 110, 7], fill=border_color, width=1)
    draw.text((5, 2), "$", fill=(50, 90, 40))
    draw.text((width-15, 2), "$", fill=(50, 90, 40))
    
    return img

def generate_money_chart(numbers, output_filename="money_chart.png"):
    """
    Строит диаграмму из стопок купюр.
    numbers: список чисел (высота стопок)
    """
    banknote = create_banknote_asset()
    b_w, b_h = banknote.size
    
    # Настройки отображения
    # Сдвиг каждой следующей купюры по вертикали (меньше высоты, чтобы было плотно)
    vertical_step = 8 
    
    # Определяем размер холста
    max_bills = max(numbers) if numbers else 0
    num_stacks = len(numbers)
    
    # Ширина холста: количество стопок * (ширина купюры + отступ)
    canvas_width = num_stacks * (b_w + 50) + 50
    # Высота холста: макс. кол-во купюр * шаг + запас
    canvas_height = max_bills * vertical_step + b_h + 100
    
    # Создаем белый фон
    canvas = Image.new('RGBA', (canvas_width, canvas_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Рисуем стопки
    current_x = 50 # Начальный отступ слева
    
    for count in numbers:
        # Рисуем снизу вверх
        base_y = canvas_height - 50 # Отступ снизу
        
        # Подписываем цифру под стопкой
        draw.text((current_x + b_w//2 - 10, base_y + 10), str(count), fill="black")
        
        # Цикл укладки купюр
        for i in range(int(count)):
            # Вычисляем Y (чем больше i, тем выше)
            y = base_y - (i * vertical_step)
            
            # Добавляем случайный сдвиг влево-вправо для реализма ("небрежная стопка")
            random_offset = random.randint(-2, 2)
            
            # Накладываем купюру
            canvas.paste(banknote, (current_x + random_offset, y), banknote)
            
        current_x += b_w + 50 # Сдвигаем X для следующей стопки
        
    # Сохраняем
    canvas.save(output_filename)
    print(f"Готово! Диаграмма сохранена как {output_filename}")

# --- ЗАПУСК ---
if __name__ == "__main__":
    # Введи сюда свои цифры
    user_input = input("Введите числа через пробел (например: 10 25 5 15): ")
    
    try:
        data = [int(x) for x in user_input.split()]
        if not data:
            print("Вы не ввели цифры.")
        else:
            generate_money_chart(data)
    except ValueError:
        print("Ошибка: вводите только целые числа.")
