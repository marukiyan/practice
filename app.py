import tkinter as tk
from tkinter import filedialog, simpledialog
import cv2
from PIL import Image, ImageTk

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор изображений")

        # Кнопки для различных операций
        self.load_button = tk.Button(root, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack(pady=10)

        self.capture_button = tk.Button(root, text="Сделать снимок с камеры", command=self.capture_from_camera)
        self.capture_button.pack(pady=10)

        self.operations_button = tk.Button(root, text="Операции с изображениями", command=self.operations)
        self.operations_button.pack(pady=10)

        self.quit_button = tk.Button(root, text="Выход", command=root.quit)
        self.quit_button.pack(pady=10)

        # Место для отображения изображения
        self.image_label = tk.Label(root)
        self.image_label.pack(padx=10, pady=10)

        self.image = None  # Переменная для хранения изображения

    def load_image(self):
        """Загружаем изображение через диалоговое окно"""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image(self.image)

    def capture_from_camera(self):
        """Снимок с камеры"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Ошибка: Не удалось подключиться к веб-камере.")
            return

        ret, frame = cap.read()
        if ret:
            cv2.imwrite("captured_image.jpg", frame)
            self.image = cv2.imread("captured_image.jpg")
            self.display_image(self.image)
        cap.release()

    def operations(self):
        """Операции с изображением"""
        if self.image is not None:
            # Показать окно для операций
            operations_window = tk.Toplevel(self.root)
            operations_window.title("Доступные операции")

            # Кнопки для операций
            rotate_button = tk.Button(operations_window, text="Повернуть", command=self.ask_rotate)
            rotate_button.pack(pady=10)

            crop_button = tk.Button(operations_window, text="Обрезать", command=self.ask_crop)
            crop_button.pack(pady=10)

            rectangle_button = tk.Button(operations_window, text="Прямоугольник", command=self.ask_rectangle)
            rectangle_button.pack(pady=10)

            red_channel_button = tk.Button(operations_window, text="Красный канал", command=lambda: self.display_channel('red'))
            red_channel_button.pack(pady=10)

            green_channel_button = tk.Button(operations_window, text="Зеленый канал", command=lambda: self.display_channel('green'))
            green_channel_button.pack(pady=10)

            blue_channel_button = tk.Button(operations_window, text="Синий канал", command=lambda: self.display_channel('blue'))
            blue_channel_button.pack(pady=10)

            back_button = tk.Button(operations_window, text="Назад", command=operations_window.destroy)
            back_button.pack(pady=10)

    def display_image(self, img):
        """Отображает изображение в окне Tkinter"""
        if img is not None:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Конвертация в RGB
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(img_pil)

            # Обновляем изображение в лейбле
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk
        else:
            print("Ошибка: Изображение не загружено.")

    def ask_rotate(self):
        """Запросить у пользователя угол для поворота"""
        angle = simpledialog.askfloat("Поворот", "Введите угол поворота изображения:")
        if angle is not None:
            self.rotate_image(angle)

    def ask_crop(self):
        """Запросить у пользователя координаты для обрезки"""
        x = simpledialog.askinteger("Обрезка", "Введите координату x:")
        y = simpledialog.askinteger("Обрезка", "Введите координату y:")
        w = simpledialog.askinteger("Обрезка", "Введите ширину:")
        h = simpledialog.askinteger("Обрезка", "Введите высоту:")
        if x is not None and y is not None and w is not None and h is not None:
            self.crop_image(x, y, w, h)

    def ask_rectangle(self):
        """Запросить у пользователя координаты для прямоугольника"""
        x = simpledialog.askinteger("Прямоугольник", "Введите координату x:")
        y = simpledialog.askinteger("Прямоугольник", "Введите координату y:")
        w = simpledialog.askinteger("Прямоугольник", "Введите ширину:")
        h = simpledialog.askinteger("Прямоугольник", "Введите высоту:")
        if x is not None and y is not None and w is not None and h is not None:
            self.draw_rectangle(x, y, w, h)

    def rotate_image(self, angle):
        """Поворот изображения"""
        if self.image is not None:
            (h, w) = self.image.shape[:2]
            center = (w // 2, h // 2)
            matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated_image = cv2.warpAffine(self.image, matrix, (w, h))
            self.display_image(rotated_image)

    def crop_image(self, x, y, w, h):
        """Обрезка изображения"""
        if self.image is not None:
            cropped_image = self.image[y:y+h, x:x+w]
            self.display_image(cropped_image)

    def draw_rectangle(self, x, y, w, h):
        """Рисование прямоугольника"""
        if self.image is not None:
            img_with_rectangle = cv2.rectangle(self.image.copy(), (x, y), (x+w, y+h), (255, 0, 0), 3)
            self.display_image(img_with_rectangle)

    def display_channel(self, channel):
        """Показывает выбранный канал (красный, зеленый, синий)"""
        if self.image is not None:
            if channel == 'red':
                channel_image = self.image[:, :, 2]  # Красный канал
            elif channel == 'green':
                channel_image = self.image[:, :, 1]  # Зеленый канал
            elif channel == 'blue':
                channel_image = self.image[:, :, 0]  # Синий канал
            else:
                print("Ошибка: Неверно выбран канал!")
                return
            # Преобразуем канал в 3D для отображения в окне
            channel_image_3d = cv2.merge([channel_image, channel_image, channel_image])
            self.display_image(channel_image_3d)

# Основная программа
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()




