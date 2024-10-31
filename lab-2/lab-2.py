import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        self.root.title("Image Processing App")

        self.original_image = None
        self.sharpened_image = None
        self.local_processed_image = None
        
        # Создаем интерфейс
        self.create_widgets()

    def create_widgets(self):
        # Кнопка для загрузки изображения
        self.general_options = tk.Frame(self.main_frame)
        self.general_options.grid(column=0, row=0)
        self.load_button = tk.Button(self.general_options, text="Загрузить изображение", command=self.load_image)
        self.load_button.grid(column=0, row=0)

        # Ползунок для параметров фильтров
        self.filter_frame = tk.Frame(self.main_frame)
        self.filter_frame.grid(column=1, row=0)
        self.sharpen_scale = ttk.Scale(self.filter_frame, from_=1, to=10, orient="horizontal", command=self.update_sharpen_param)
        self.sharpen_scale.set(3)
        self.sharpen_scale.grid(column=0, row=1)
        self.sharpen_param_label = tk.Label(self.filter_frame, text="Параметр резкости:")
        self.sharpen_param_label.grid(column=0, row=0)

        self.sharpen_filter_type_var = tk.StringVar(value="Лаплассиан")
        self.sharpen_filter_type = ttk.Combobox(self.filter_frame, textvariable=self.sharpen_filter_type_var,
                                                values=[
                                                    "Лаплассиан","LoG"
                                                ])
        self.sharpen_filter_type.grid(column=0, row=0)
        self.sharpen_filter_type.bind("<<ComboboxSelected>>", self.on_sharpen_filter_type_combobox)
        # Кнопка для применения фильтра резкости
        self.sharpen_button = tk.Button(self.filter_frame, text="Применить фильтр резкости", command=self.apply_sharpen_filter)
        self.sharpen_button.grid(column=0, row=2)
        self.save_sharpen_button = tk.Button(self.filter_frame, text="Сохранить эту картинку", command=self.save_sharpened_image)
        self.save_sharpen_button.grid(column=0, row=3)

        self.threshold_frame = tk.Frame(self.main_frame)
        self.threshold_frame.grid(column=2, row=0)
        # Выпадающий список для локальной обработки
        self.local_processing_var = tk.StringVar(value="adaptive thresholding")
        self.local_processing_menu = ttk.Combobox(self.threshold_frame, textvariable=self.local_processing_var,
                                                    values=["Otsu's method", "adaptive thresholding"])
        self.local_processing_menu.grid(column=0, row=1)
        self.save_local_processed_button = tk.Button(self.threshold_frame, text="Сохранить эту картинку", command=self.save_local_processed_image)
        self.save_local_processed_button.grid(column=0, row=3)
        self.local_processing_menu.bind("<<ComboboxSelected>>", self.on_adaptive_processing_combobox)
        self.adaptive_threshold_modes_var = tk.StringVar(value='mean')
        self.adaptive_thresholding_modes = ttk.Combobox(root, textvariable=self.adaptive_threshold_modes_var, 
                                                        values=['mean', 'gaussian'])
        #self.adaptive_thresholding_modes.grid(column=0, row=2)
        # Ползунок для параметров пороговой обработки
        self.threshold_scale = ttk.Scale(self.root, from_=0, to=255, orient="horizontal", command=self.update_threshold_param)
        self.threshold_scale.set(128)
#        self.threshold_scale.pack()
        self.threshold_param_label = tk.Label(self.threshold_frame, text="Пороговое значение:")
        self.threshold_param_label.grid(column=0, row=0)

        # Кнопка для применения локальной обработки
        self.apply_local_button = tk.Button(self.threshold_frame, text="Применить локальную обработку", command=self.apply_local_processing)
        self.apply_local_button.grid(column=0, row=2)

        # Кнопка для сброса фильтров и локальной обработки
        self.reset_button = tk.Button(self.general_options, text="Сбросить изменения", command=self.reset_images)
        self.reset_button.grid(column=0, row=1)

        # Область для отображения изображений
        self.canvas = tk.Canvas(self.main_frame, width=1200, height=600)
        self.canvas.grid(row=1, columnspan=3)
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

    def apply_sharpen_filter(self):
        # Проверим, что изображение и тип фильтра заданы
        if self.original_image is None:
            messagebox.showerror("Ошибка", "Загрузите изображение для обработки.")
            return

        if not self.sharpen_filter_type:
            messagebox.showerror("Ошибка", "Выберите тип фильтра.")
            return

#        image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
         # Значение степени резкости от пользователя
        sharpen_amount = int(self.sharpen_scale.get())

        # Значение ядра должно быть нечетным и >= 3
        kernel_size = max(3, sharpen_amount | 1)  # Приводим к нечетному числу

        # Применение фильтра на основе выбранного типа
        if self.sharpen_filter_type_var.get() == "Лаплассиан":
            self.sharpened_image = self.apply_laplacian(image)
            self.display_image(self.original_image)
        elif self.sharpen_filter_type_var.get() == "LoG":
            self.sharpened_image = self.apply_log_filter(image, kernel_size=kernel_size)
            self.display_image(self.original_image)
        else:
            messagebox.showwarning("Внимание", "Неизвестный тип фильтра. Попробуйте снова.")
            return

    def apply_laplacian(self, image):
        """Применение фильтра Лапласиана для выделения контуров."""
        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        min_val, max_val = np.min(laplacian), np.max(laplacian)
        normalized = 255 * (laplacian - min_val) / (max_val - min_val)
        return cv2.convertScaleAbs(normalized)

    def apply_log_filter(self, image, kernel_size=5, sigma=1.0):
        # Размытие Гаусса для подавления шума
        blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

        # Применение Лапласиана к размытому изображению
        log = cv2.Laplacian(blurred, cv2.CV_64F)

         # Нормализация значений, чтобы избежать потери данных
        min_val, max_val = np.min(log), np.max(log)
        log_normalized = 255 * (log - min_val) / (max_val - min_val)

        # Преобразование в 8-битный формат для отображения
        return cv2.convertScaleAbs(log_normalized)

    def on_adaptive_processing_combobox(self, event):
        self.apply_local_processing()

    def on_sharpen_filter_type_combobox(self, event):
        self.apply_sharpen_filter()

    def apply_local_processing(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Сначала загрузите изображение!")
            return

        threshold_value = int(self.threshold_scale.get())
        
        if self.local_processing_var.get() == "Otsu's method":
    #        self.adaptive_thresholding_modes.state(tk.DISABLED)
            gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
            _, self.local_processed_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            #self.adaptive_thresholding_modes.grid_remove()
            self.display_image(self.original_image)
        elif self.local_processing_var.get() == "adaptive thresholding":
            #self.adaptive_thresholding_modes.grid()
     #       self.adaptive_thresholding_modes.state(tk.ACTIVE)
            gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2GRAY)
            if self.adaptive_threshold_modes_var.get() == 'mean':
                self.local_processed_image = cv2.adaptiveThreshold(gray_image, 255,
                                                            cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
                self.display_image(self.original_image)
            elif self.adaptive_threshold_modes_var.get() == 'gaussian':
                self.local_processed_image = cv2.adaptiveThreshold(gray_image, 255,
                                                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                self.display_image(self.original_image)

    def update_sharpen_param(self, value):
        self.sharpen_param_label.config(text=f"Параметр резкости: {int(float(value))}")
        self.apply_sharpen_filter()

    def update_threshold_param(self, value):
        self.threshold_param_label.config(text=f"Пороговое значение: {int(float(value))}")
        self.apply_local_processing()

    def save_sharpened_image(self):
        cv2.imwrite('sharpened_image.png', self.sharpened_image)
    def save_local_processed_image(self):
        cv2.imwrite('local_processed_image.png', self.local_processed_image)

    def reset_images(self):
        if self.original_image is not None:
            self.sharpened_image = self.original_image.copy()
            self.local_processed_image = self.original_image.copy()
            self.display_image(self.original_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()