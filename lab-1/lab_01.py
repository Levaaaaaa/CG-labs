import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QLineEdit, \
    QColorDialog, QFrame


class ColorConverterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("RGB to CMYK & HSV Converter")
        self.setGeometry(100, 100, 1000, 500)

        layout = QVBoxLayout()

        # RGBBBBBBBBBBBBBBBBBBBBBB
        self.rgb_label = QLabel("RGB Input")
        layout.addWidget(self.rgb_label)

        self.rgb_sliders_layout = QHBoxLayout()
        self.r_slider, self.r_input = self.create_rgb_control("R")
        self.g_slider, self.g_input = self.create_rgb_control("G")
        self.b_slider, self.b_input = self.create_rgb_control("B")

        self.rgb_sliders_layout.addWidget(self.r_slider)
        self.rgb_sliders_layout.addWidget(self.g_slider)
        self.rgb_sliders_layout.addWidget(self.b_slider)

        layout.addLayout(self.rgb_sliders_layout)

        self.rgb_inputs_layout = QHBoxLayout()
        self.rgb_inputs_layout.addWidget(self.r_input)
        self.rgb_inputs_layout.addWidget(self.g_input)
        self.rgb_inputs_layout.addWidget(self.b_input)
        layout.addLayout(self.rgb_inputs_layout)
        # RGBBBBBBBBBBBBBBBBBBBBBBBBBBBB

        # CMYKKKKKKKKKKKKKKKKKKKKKKK
        self.cmyk_label = QLabel("CMYK Input")
        layout.addWidget(self.cmyk_label)

        self.cmyk_sliders_layout = QHBoxLayout()
        self.c_slider, self.c_input = self.create_cmyk_control("C")
        self.m_slider, self.m_input = self.create_cmyk_control("M")
        self.y_slider, self.y_input = self.create_cmyk_control("Y")
        self.k_slider, self.k_input = self.create_cmyk_control("K")

        self.cmyk_sliders_layout.addWidget(self.c_slider)
        self.cmyk_sliders_layout.addWidget(self.m_slider)
        self.cmyk_sliders_layout.addWidget(self.y_slider)
        self.cmyk_sliders_layout.addWidget(self.k_slider)

        layout.addLayout(self.cmyk_sliders_layout)

        self.cmyk_inputs_layout = QHBoxLayout()
        self.cmyk_inputs_layout.addWidget(self.c_input)
        self.cmyk_inputs_layout.addWidget(self.m_input)
        self.cmyk_inputs_layout.addWidget(self.y_input)
        self.cmyk_inputs_layout.addWidget(self.k_input)

        layout.addLayout(self.cmyk_inputs_layout)
        # CMYKKKKKKKKKKKKKKKKKKKKKKKKKK

        # HSVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
        self.hsv_label = QLabel("HSV Input")
        layout.addWidget(self.hsv_label)

        self.hsv_sliders_layout = QHBoxLayout()
        self.h_slider, self.h_input = self.create_hsv_control("H")
        self.s_slider, self.s_input = self.create_hsv_control("S")
        self.v_slider, self.v_input = self.create_hsv_control("V")

        self.hsv_sliders_layout.addWidget(self.h_slider)
        self.hsv_sliders_layout.addWidget(self.s_slider)
        self.hsv_sliders_layout.addWidget(self.v_slider)

        layout.addLayout(self.hsv_sliders_layout)

        self.hsv_inputs_layout = QHBoxLayout()
        self.hsv_inputs_layout.addWidget(self.h_input)
        self.hsv_inputs_layout.addWidget(self.s_input)
        self.hsv_inputs_layout.addWidget(self.v_input)
        layout.addLayout(self.hsv_inputs_layout)
        # HSVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV

        self.palette_button = QPushButton("Choose Color from Palette")
        self.palette_button.clicked.connect(self.choose_color_from_palette)
        layout.addWidget(self.palette_button)

        self.color_preview_label = QLabel("Color Preview")
        layout.addWidget(self.color_preview_label)

        self.color_preview = QFrame()
        self.color_preview.setFixedSize(100, 100)
        self.color_preview.setStyleSheet("background-color: rgb(128, 128, 128);")
        layout.addWidget(self.color_preview)

        self.setLayout(layout)

        self.update_cmyk_output(_from="rgb")

    def create_rgb_control(self, label_text):
        layout = QVBoxLayout()
        label = QLabel(f"{label_text}:")
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(255)
        slider.setValue(128)
        slider.valueChanged.connect(self.update_rgb_from_slider)

        input_field = QLineEdit()
        input_field.setText("128")
        input_field.setFixedWidth(50)
        input_field.returnPressed.connect(self.update_rgb_from_input)

        layout.addWidget(label)
        layout.addWidget(slider)
        return slider, input_field

    def create_cmyk_control(self, label_text):
        layout = QVBoxLayout()
        label = QLabel(f"{label_text}:")

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(0)
        slider.valueChanged.connect(self.update_cmyk_from_slider)

        input_field = QLineEdit()
        input_field.setText("0")
        input_field.setFixedWidth(50)
        input_field.returnPressed.connect(self.update_cmyk_from_input)

        layout.addWidget(label)
        layout.addWidget(slider)

        return slider, input_field

    def create_hsv_control(self, label_text):
        layout = QVBoxLayout()
        label = QLabel(f"{label_text}:")

        if label_text == "H":
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(360)
            slider.setValue(180)
            slider.valueChanged.connect(self.update_hsv_from_slider)
        else:
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(50)
            slider.valueChanged.connect(self.update_hsv_from_slider)

        input_field = QLineEdit()
        input_field.setText("180" if label_text == "H" else "50")
        input_field.setFixedWidth(50)
        input_field.returnPressed.connect(self.update_hsv_from_input)

        layout.addWidget(label)
        layout.addWidget(slider)

        return slider, input_field

    def update_rgb_from_slider(self):
        r = self.r_slider.value()
        g = self.g_slider.value()
        b = self.b_slider.value()

        self.r_input.setText(str(r))
        self.g_input.setText(str(g))
        self.b_input.setText(str(b))

        self.update_cmyk_output(_from="rgb")
        self.update_hsv_output(_from="rgb")

    def update_rgb_from_input(self):
        try:
            r = int(self.r_input.text())
            g = int(self.g_input.text())
            b = int(self.b_input.text())
        except ValueError:
            return

        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))

        if str(r) != self.r_input.text():
            self.r_input.setText(str(r))
        if str(g) != self.g_input.text():
            self.g_input.setText(str(g))
        if str(b) != self.b_input.text():
            self.b_input.setText(str(b))

        sliders = [self.r_slider, self.g_slider, self.b_slider]
        self.disable_signals(sliders)
        self.r_slider.setValue(r)
        self.g_slider.setValue(g)
        self.b_slider.setValue(b)
        self.enable_signals(sliders)

        self.update_cmyk_output(_from="rgb")
        self.update_hsv_output(_from="rgb")

    def update_cmyk_from_slider(self):
        c = self.c_slider.value()
        m = self.m_slider.value()
        y = self.y_slider.value()
        k = self.k_slider.value()

        self.c_input.setText(str(c))
        self.m_input.setText(str(m))
        self.y_input.setText(str(y))
        self.k_input.setText(str(k))

        self.update_rgb_output(_from="cmyk")
        self.update_hsv_output(_from="cmyk")

    def update_cmyk_from_input(self):
        try:
            c = int(self.c_input.text())
            m = int(self.m_input.text())
            y = int(self.y_input.text())
            k = int(self.k_input.text())
        except ValueError:
            return

        c = max(0, min(c, 100))
        m = max(0, min(m, 100))
        y = max(0, min(y, 100))
        k = max(0, min(k, 100))

        if str(c) != self.c_input.text():
            self.c_input.setText(str(c))
        if str(m) != self.m_input.text():
            self.m_input.setText(str(m))
        if str(y) != self.y_input.text():
            self.y_input.setText(str(y))
        if str(k) != self.k_input.text():
            self.k_input.setText(str(k))

        sliders = [self.c_slider, self.m_slider, self.y_slider, self.k_slider]
        self.disable_signals(sliders)
        self.c_slider.setValue(c)
        self.m_slider.setValue(m)
        self.y_slider.setValue(y)
        self.k_slider.setValue(k)
        self.enable_signals(sliders)

        self.update_rgb_output(_from="cmyk")
        self.update_hsv_output(_from="cmyk")

    def update_hsv_from_slider(self):
        h = self.h_slider.value()
        s = self.s_slider.value()
        v = self.v_slider.value()

        self.h_input.setText(str(h))
        self.s_input.setText(str(s))
        self.v_input.setText(str(v))

        self.update_rgb_output(_from="hsv")
        self.update_cmyk_output(_from="hsv")

    def update_hsv_from_input(self):
        try:
            h = int(self.h_input.text())
            s = int(self.s_input.text())
            v = int(self.v_input.text())
        except ValueError:
            return

        h = max(0, min(h, 360))
        s = max(0, min(s, 100))
        v = max(0, min(v, 100))
        if str(h) != self.h_input.text():
            self.h_input.setText(str(h))
        if str(s) != self.s_input.text():
            self.s_input.setText(str(s))
        if str(v) != self.v_input.text():
            self.v_input.setText(str(v))

        sliders = [self.h_slider, self.s_slider, self.v_slider]
        self.disable_signals(sliders)
        self.h_slider.setValue(h)
        self.s_slider.setValue(s)
        self.v_slider.setValue(v)
        self.enable_signals(sliders)

        self.update_rgb_output(_from="hsv")
        self.update_cmyk_output(_from="hsv")

    def update_rgb_output(self, _from: str):
        r, g, b = None, None, None
        if _from == "cmyk":
            c = self.c_slider.value() / 100.0
            m = self.m_slider.value() / 100.0
            y = self.y_slider.value() / 100.0
            k = self.k_slider.value() / 100.0

            r = 255 * (1 - c) * (1 - k)
            g = 255 * (1 - m) * (1 - k)
            b = 255 * (1 - y) * (1 - k)
        elif _from == "hsv":
            h = self.h_slider.value()
            s = self.s_slider.value() / 100.0
            v = self.v_slider.value() / 100.0

            h = h % 360

            if s == 0:
                r = g = b = v * 255
            else:
                c = v * s
                x = c * (1 - abs((h / 60) % 2 - 1))
                m = v - c

                if 0 <= h < 60:
                    r, g, b = c, x, 0
                elif 60 <= h < 120:
                    r, g, b = x, c, 0
                elif 120 <= h < 180:
                    r, g, b = 0, c, x
                elif 180 <= h < 240:
                    r, g, b = 0, x, c
                elif 240 <= h < 300:
                    r, g, b = x, 0, c
                elif 300 <= h < 360:
                    r, g, b = c, 0, x

                r = (r + m) * 255
                g = (g + m) * 255
                b = (b + m) * 255

        sliders = [self.r_slider, self.g_slider, self.b_slider]
        self.disable_signals(sliders)
        self.r_slider.setValue(int(r))
        self.g_slider.setValue(int(g))
        self.b_slider.setValue(int(b))
        self.enable_signals(sliders)

        self.r_input.setText(f"{int(r)}")
        self.g_input.setText(f"{int(g)}")
        self.b_input.setText(f"{int(b)}")

        self.color_preview.setStyleSheet(f"background-color: rgb({int(r)}, {int(g)}, {int(b)});")

    def update_cmyk_output(self, _from: str):
        if _from == "rgb":
            r = self.r_slider.value() / 255.0
            g = self.g_slider.value() / 255.0
            b = self.b_slider.value() / 255.0
        elif _from == "hsv":
            h = self.h_slider.value() % 360
            s = self.s_slider.value() / 100.0
            v = self.v_slider.value() / 100.0

            if s == 0:
                r = g = b = v
            else:
                i = int(h / 60) % 6
                f = (h / 60) - i
                p = v * (1 - s)
                q = v * (1 - f * s)
                t = v * (1 - (1 - f) * s)

                if i == 0:
                    r, g, b = v, t, p
                elif i == 1:
                    r, g, b = q, v, p
                elif i == 2:
                    r, g, b = p, v, t
                elif i == 3:
                    r, g, b = p, q, v
                elif i == 4:
                    r, g, b = t, p, v
                elif i == 5:
                    r, g, b = v, p, q

        k = 1 - max(r, g, b)
        if k < 1:
            c = (1 - r - k) / (1 - k)
            m = (1 - g - k) / (1 - k)
            y = (1 - b - k) / (1 - k)
        else:
            c = m = y = 0

        self.c_input.setText(f"{c * 100:.0f}")
        self.m_input.setText(f"{m * 100:.0f}")
        self.y_input.setText(f"{y * 100:.0f}")
        self.k_input.setText(f"{k * 100:.0f}")

        sliders = [self.c_slider, self.m_slider, self.y_slider, self.k_slider]
        self.disable_signals(sliders)
        self.c_slider.setValue(int(c * 100))
        self.m_slider.setValue(int(m * 100))
        self.y_slider.setValue(int(y * 100))
        self.k_slider.setValue(int(k * 100))
        self.enable_signals(sliders)

        self.color_preview.setStyleSheet(f"background-color: rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)});")

    def update_hsv_output(self, _from: str):
        if _from == "rgb":
            r = self.r_slider.value() / 255.0
            g = self.g_slider.value() / 255.0
            b = self.b_slider.value() / 255.0
        elif _from == "cmyk":
            c = self.c_slider.value() / 100.0
            m = self.m_slider.value() / 100.0
            y = self.y_slider.value() / 100.0
            k = self.k_slider.value() / 100.0

            r = (1 - c) * (1 - k)
            g = (1 - m) * (1 - k)
            b = (1 - y) * (1 - k)

        mx = max(r, g, b)
        mn = min(r, g, b)
        diff = mx - mn

        if diff == 0:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / diff) + 120) % 360
        else:
            h = (60 * ((r - g) / diff) + 240) % 360

        s = 0 if mx == 0 else (diff / mx) * 100

        v = mx * 100

        self.h_input.setText(f"{int(h)}")
        self.s_input.setText(f"{int(s)}")
        self.v_input.setText(f"{int(v)}")

        sliders = [self.h_slider, self.s_slider, self.v_slider]
        self.disable_signals(sliders)
        self.h_slider.setValue(int(h))
        self.s_slider.setValue(int(s))
        self.v_slider.setValue(int(v))
        self.enable_signals(sliders)

        self.color_preview.setStyleSheet(f"background-color: rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)});")

    def choose_color_from_palette(self):
        color = QColorDialog.getColor()

        if color.isValid():
            r, g, b, _ = color.getRgb()
            self.r_slider.setValue(r)
            self.g_slider.setValue(g)
            self.b_slider.setValue(b)

            self.update_rgb_from_slider()

    @staticmethod
    def disable_signals(signals: list):
        for signal in signals:
            signal.blockSignals(True)

    @staticmethod
    def enable_signals(signals: list):
        for signal in signals:
            signal.blockSignals(False)

    @staticmethod
    def round(number):
        return int(number) + 1 if (number * 10) % 10 >= 5 else int(number)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = ColorConverterApp()
    converter.show()
    sys.exit(app.exec_())
