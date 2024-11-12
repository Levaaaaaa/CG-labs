import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")
        
        self.original_image = None
        self.sharpened_image = None
        self.local_processed_image = None
        
        # Создаем интерфейс
        self.create_widgets()

    def create_widgets(self):
        # Кнопка для загрузки изображения
        self.load_button = tk.Button(self.root, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack()

        # Ползунок для параметров фильтров
        self.sharpen_scale = ttk.Scale(self.root, from_=1, to=10, orient="horizontal", command=self.update_sharpen_param)
        self.sharpen_scale.set(3)
        self.sharpen_scale.pack()
        self.sharpen_param_label = tk.Label(self.root, text="Параметр резкости:")
        self.sharpen_param_label.pack()

        # Кнопка для применения фильтра резкости
        self.sharpen_button = tk.Button(self.root, text="Применить фильтр резкости", command=self.apply_sharpen_filter)
        self.sharpen_button.pack()

        # Выпадающий список для локальной обработки
        self.local_processing_var = tk.StringVar(value="Пороговая обработка")
        self.local_processing_menu = ttk.Combobox(self.root, textvariable=self.local_processing_var,
                                                    values=["Адаптивная обработка", "Устойчивый порог"])
        self.local_processing_menu.pack()

    
        # Ползунок для параметров пороговой обработки
        self.threshold_scale = ttk.Scale(self.root, from_=0, to=255, orient="horizontal", command=self.update_threshold_param)
        self.threshold_scale.set(128)
        self.threshold_scale.pack()
        self.threshold_param_label = tk.Label(self.root, text="Пороговое значение:")
        self.threshold_param_label.pack()

        # Кнопка для применения локальной обработки
        self.apply_local_button = tk.Button(self.root, text="Применить локальную обработку", command=self.apply_local_processing)
        self.apply_local_button.pack()

        # Кнопка для сброса фильтров и локальной обработки
        self.reset_button = tk.Button(self.root, text="Сбросить изменения", command=self.reset_images)
        self.reset_button.pack()

        # Область для отображения изображений
        self.canvas = tk.Canvas(self.root, width=1200, height=600)
        self.canvas.pack()
        self.img_w = 400
        self.img_h = 600

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.sharpened_image = self.original_image.copy()
            self.local_processed_image = self.original_image.copy()
            self.display_image(self.original_image)

    def display_image(self, img):
        img = Image.fromarray(img).resize((self.img_w, self.img_h))
        img_tk = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0, 0, anchor="nw", image=img_tk)
        self.canvas.img = img_tk

        # Display original, sharpened and local processed images
        self.canvas.delete("all")
        if self.original_image is not None:
            self.canvas.create_image(0, 0, anchor="nw", image=img_tk)

        if self.sharpened_image is not None:
            sharpened_img = Image.fromarray(self.sharpened_image).resize((self.img_w, self.img_h))
            sharpened_img_tk = ImageTk.PhotoImage(image=sharpened_img)
            self.canvas.create_image(self.img_w, 0, anchor="nw", image=sharpened_img_tk)
            self.canvas.img2 = sharpened_img_tk

        if self.local_processed_image is not None:
            local_processed_img = Image.fromarray(self.local_processed_image).resize((self.img_w, self.img_h))
            local_processed_img_tk = ImageTk.PhotoImage(image=local_processed_img)
            self.canvas.create_image(2 * self.img_w, 0, anchor="nw", image=local_processed_img_tk)
            self.canvas.img3 = local_processed_img_tk

    def on_local_processing_combobox(self, event):
        self.apply_local_processing()

    def apply_sharpen_filter(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Сначала загрузите изображение!")
            return

        # Фильтр резкости
        sharpen_amount = int(self.sharpen_scale.get())
        kernel = np.array([[0, -1, 0], [-1, 5 + sharpen_amount, -1], [0, -1, 0]])
        self.sharpened_image = cv2.filter2D(self.original_image, -1, kernel)
        self.display_image(self.original_image)

    def apply_local_processing(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Сначала загрузите изображение!")
            return

        threshold_value = int(self.threshold_scale.get())
        
        if self.local_processing_var.get() == "Пороговая обработка":
            gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
            _, self.local_processed_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
        elif self.local_processing_var.get() == "Устойчивый порог":
            gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
            self.local_processed_image = cv2.adaptiveThreshold(gray_image, 255,
                                                            cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        self.display_image(self.original_image)

    def update_sharpen_param(self, value):
        self.sharpen_param_label.config(text=f"Параметр резкости: {int(float(value))}")
        self.apply_sharpen_filter()

    def update_threshold_param(self, value):
        self.threshold_param_label.config(text=f"Пороговое значение: {int(float(value))}")
        self.apply_local_processing()

    def reset_images(self):
        if self.original_image is not None:
            self.sharpened_image = self.original_image.copy()
            self.local_processed_image = self.original_image.copy()
            self.display_image(self.original_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()