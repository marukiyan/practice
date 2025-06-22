import cv2
import numpy as np

def load_image(image_path):
    """Загружает изображение из файла."""
    return cv2.imread(image_path)

def show_image(image, window_name="Image"):
    """Отображает изображение в окне."""
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def change_size(image, width, height):
    """Изменяет размер изображения."""
    return cv2.resize(image, (width, height))

def crop_image(image, x, y, w, h):
    """Обрезает изображение."""
    return image[y:y+h, x:x+w]

def invert_image(image):
    """Создает негатив изображения."""
    return cv2.bitwise_not(image)

def process_image():
    """Основной процесс, где будут использоваться функции."""
    # Замените путь к изображению
    image_path = 'C:\\Users\\Huawei\\Pictures\\my_image.jpg'
    img = load_image(image_path)

    # Отображаем оригинальное изображение
    show_image(img, "Original Image")

    # Ввод от пользователя
    action = input("Choose action: (1) Change size, (2) Crop, (3) Invert: ")

    if action == "1":
        width = int(input("Enter new width: "))
        height = int(input("Enter new height: "))
        img_resized = change_size(img, width, height)
        show_image(img_resized, "Resized Image")

    elif action == "2":
        x = int(input("Enter x coordinate: "))
        y = int(input("Enter y coordinate: "))
        w = int(input("Enter width: "))
        h = int(input("Enter height: "))
        img_cropped = crop_image(img, x, y, w, h)
        show_image(img_cropped, "Cropped Image")

    elif action == "3":
        img_inverted = invert_image(img)
        show_image(img_inverted, "Inverted Image")

    else:
        print("Invalid option!")

# Запуск процесса
process_image()
