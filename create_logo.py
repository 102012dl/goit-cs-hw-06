from PIL import Image, ImageDraw, ImageFont

# Створення порожнього білого зображення
width, height = 200, 100
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Додавання тексту до зображення
text = "Logo"
font = ImageFont.load_default()
textwidth, textheight = draw.textsize(text, font)

# Розміщення тексту по центру зображення
x = (width - textwidth) / 2
y = (height - textheight) / 2
draw.text((x, y), text, fill="black", font=font)

# Збереження зображення
image.save("static/logo.png")



Запуск 

bash 

python create_logo.py
