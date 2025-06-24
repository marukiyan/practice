import cv2
import numpy as np
import os


def load_image(image_path):
    """Загружает изображение из файла."""
    if os.path.exists(image_path):
        print(f"Файл найден: {image_path}")
        img = cv2.imread(image_path)
        if img is None:
            print("Ошибка: Файл не является изображением или поврежден!")
            return None
        print(f"Изображение загружено. Размер: {img.shape}")
        return img
    else:
        print("Ошибка: Файл не найден!")
        return None


def capture_from_camera():
    """Захват изображения с веб-камеры."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Ошибка: Не удалось подключиться к веб-камере.")
        print("Проверьте, подключена ли камера, а также попробуйте закрыть другие приложения, использующие камеру.")
        return None

    print("Нажмите 's', чтобы сделать снимок.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка: Не удалось захватить изображение с веб-камеры.")
            break

        cv2.imshow('WebCam - Press "s" to capture', frame)

        # Нажатие клавиши 's' для сохранения изображения
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite('captured_image.jpg', frame)
            print("Снимок сохранен как 'captured_image.jpg'.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return cv2.imread('captured_image.jpg')  # Возвращаем сохранённое изображение


def show_image(image, window_name="Изображение"):
    """Отображает изображение в окне."""
    if image is not None:
        cv2.imshow(window_name, image)
        cv2.waitKey(0)  # Ожидает, пока не нажмете клавишу, чтобы закрыть окно
        cv2.destroyAllWindows()
    else:
        print("Ошибка: Изображение не загружено.")


def display_channel(image, channel):
    """Показывает только выбранный канал (красный, зеленый или синий)."""
    if channel == 'red':
        channel_image = image[:, :, 2]  # Красный канал
    elif channel == 'green':
        channel_image = image[:, :, 1]  # Зеленый канал
    elif channel == 'blue':
        channel_image = image[:, :, 0]  # Синий канал
    else:
        print("Ошибка: Неверно выбран канал!")
        return None
    # Преобразуем канал в 3D для отображения в окне
    channel_image_3d = cv2.merge([channel_image, channel_image, channel_image])
    return channel_image_3d


def crop_image(image, x, y, w, h):
    """Обрезает изображение по заданным координатам."""
    image_height, image_width = image.shape[:2]
    if x + w > image_width or y + h > image_height:
        print("Ошибка: Координаты обрезки выходят за пределы изображения.")
        return None
    return image[y:y + h, x:x + w]


def draw_rectangle(image, x, y, w, h):
    """Нарисовать прямоугольник синим цветом."""
    return cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Цвет синий (BGR)


def rotate_image(image, angle):
    """Вращает изображение на заданный угол."""
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)  # Центр изображения
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)  # Получаем матрицу вращения
    rotated_image = cv2.warpAffine(image, matrix, (w, h))  # Поворачиваем изображение
    return rotated_image


def process_image():
    """Основной процесс, где будут использоваться функции."""
    choice = input(
        "Выберите способ загрузки изображения:\n1. Загрузить изображение с диска\n2. Сделать снимок с веб-камеры\nВведите 1 или 2: ")

    if choice == '1':
        image_path = input("Введите путь к изображению (формат png или jpg): ")
        img = load_image(image_path)
    elif choice == '2':
        img = capture_from_camera()
    else:
        print("Ошибка: Неверный выбор!")
        return

    if img is None:
        print("Программа завершена, так как изображение не удалось загрузить.")
        return

    # Отображаем оригинальное изображение
    show_image(img, "Оригинальное изображение")

    # Ввод от пользователя для выбора канала
    while True:
        channel = input("Введите канал для отображения (red, green, blue): ").lower()
        if channel in ['red', 'green', 'blue']:
            break
        else:
            print("Ошибка: Неверный выбор канала! Попробуйте снова.")

    img_channel = display_channel(img, channel)

    if img_channel is not None:
        show_image(img_channel, f"Канал: {channel.capitalize()}")

    # Ввод для обрезки изображения
    while True:
        action = input("Выберите действие: (1) Обрезать, (2) Нарисовать прямоугольник, (3) Вращение: ")
        if action == "1":
            try:
                x = int(input("Введите координату x: "))
                y = int(input("Введите координату y: "))
                w = int(input("Введите ширину: "))
                h = int(input("Введите высоту: "))
                img_cropped = crop_image(img, x, y, w, h)
                if img_cropped is not None:
                    show_image(img_cropped, "Обрезанное изображение")
                break
            except ValueError:
                print("Ошибка: Пожалуйста, вводите только числа.")
        elif action == "2":
            try:
                x = int(input("Введите координату x прямоугольника: "))
                y = int(input("Введите координату y прямоугольника: "))
                w = int(input("Введите ширину прямоугольника: "))
                h = int(input("Введите высоту прямоугольника: "))
                img_with_rectangle = draw_rectangle(img, x, y, w, h)
                show_image(img_with_rectangle, "Изображение с прямоугольником")
                break
            except ValueError:
                print("Ошибка: Пожалуйста, вводите только числа.")
        elif action == "3":
            try:
                angle = float(input("Введите угол вращения: "))
                img_rotated = rotate_image(img, angle)
                show_image(img_rotated, "Вращённое изображение")
                break
            except ValueError:
                print("Ошибка: Пожалуйста, введите корректное число для угла.")
        else:
            print("Ошибка: Неверный выбор действия! Попробуйте снова.")


# Запуск процесса
process_image()



