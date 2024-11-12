import tkinter as tk
from tkinter import colorchooser
import colorsys as cs

RGB_SCALE=255
CMYK_SCALE=100

def cmyk_to_rgb(c, m,y,k):
    c1 = c / CMYK_SCALE
    m1 = m / CMYK_SCALE
    y1 = y / CMYK_SCALE
    k1 = k / CMYK_SCALE

    r = round(RGB_SCALE - ((min(1.0, c1 * (1.0 - k))) * RGB_SCALE))
    g = round(RGB_SCALE - ((min(1.0, m1 * (1.0 - k))) * RGB_SCALE))
    b = round(RGB_SCALE - ((min(1.0, y1 * (1.0 - k))) * RGB_SCALE))

    return (r, g, b)

def rgb_to_cmyk(r, g, b):
    r /= 255.0
    g /= 255.0
    b /= 255.0
    k = 1 - max(r, g, b)
    if k == 1:
        return (0, 0, 0, 1)
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return (c, m, y, k)

def hsl_to_rgb(h, l, s):
    rgb = cs.hls_to_rgb(h,l,s)
    return (rgb[0], rgb[1], rgb[2])

def rgb_to_hsl(r, g, b):
    r /= 255
    g /= 255
    b /= 255
    max_ = max([r, g, b])
    min_ = min([r, g, b])

    if max_ == min_:
        h = 0
    elif max_ == r:
        h = 60 * (g - b) / (max_ - min_) + 360 if g < b else 0
    elif max_ == g:
        h = 60 * (b-r) / (max_ - min_) + 120
    else:
        h = 60 * (r - g) / (max_ - min_) + 240

    l = (max_ + min_) / 2
    
    if l==0 or max_==min_:
        s = 0
    else :
        s = (max_ - min_) / (1 - abs(1 - (max_ + min_)))    
    return (h, s * 100, l*100)

    

def update_colors(r, g, b):
    # Update CMYK
    c, m, y, k = rgb_to_cmyk(r, g, b)
    update_cmyk(c,m,y,k)

    # Update HSL
    h, s, l = rgb_to_hsl(r, g, b)
    update_hsl(h,s,l)
    # Update background color
    color_box.config(bg=f'#{r:02x}{g:02x}{b:02x}')

    update_rgb(r, g, b)

def update_cmyk(c,m,y,k):
    cmyk_label.config(text=f'CMYK: {c:.2f}, {m:.2f}, {y:.2f}, {k:.2f}')
    c_spinbox.delete(0, "end")
    c_spinbox.insert(0, str(c))
    m_spinbox.delete(0, "end")
    m_spinbox.insert(0, str(m))
    y_spinbox.delete(0, "end")
    y_spinbox.insert(0, str(y))
    k_spinbox.delete(0, "end")
    k_spinbox.insert(0, str(k))

def update_rgb(r,g,b):
    
    #update sliders
    r_slider.set(r)
    g_slider.set(g)
    b_slider.set(b)

    #update spinboxes
    r_spinbox.delete(0, "end")
    r_spinbox.insert(0, str(r))
    g_spinbox.delete(0, "end")
    g_spinbox.insert(0, str(g))
    b_spinbox.delete(0, "end")
    b_spinbox.insert(0, str(b))

def update_hsl(h, s, l):
    h_spinbox.delete(0, "end")
    h_spinbox.insert(0, str(h))
    s_spinbox.delete(0, "end")
    s_spinbox.insert(0, str(s))
    l_spinbox.delete(0, "end")
    l_spinbox.insert(0, str(l))
    hsl_label.config(text=f'HSL: {h:.2f}, {s:.2f}, {l:.2f}')

#палитра
def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code:
        rgb = color_code[0]
        r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
        r_spinbox.delete(0, tk.END)
        r_spinbox.insert(0, str(r))
        g_spinbox.delete(0, tk.END)
        g_spinbox.insert(0, str(g))
        b_spinbox.delete(0, tk.END)
        b_spinbox.insert(0, str(b))
        update_colors(r, g, b)

#spinboxes
def on_spinbox_change():
    try:
    
        r = int(r_spinbox.get())
        #print(event.widget)
        g = int(g_spinbox.get())
        b = int(b_spinbox.get())
        update_colors(r, g, b)
    except ValueError:
        pass

def on_spinbox_change_for_bind(event):
    try:
    
        r = int(r_spinbox.get())
        #print(event.widget)
        g = int(g_spinbox.get())
        b = int(b_spinbox.get())
        update_colors(r, g, b)
    except ValueError:
        pass

def on_cmyk_spinbox_change():
    try:
        c = int(c_spinbox.get())
        m = int(m_spinbox.get())
        y = int(y_spinbox.get())
        k = int(k_spinbox.get())
        r, g, b = cmyk_to_rgb(c, m, y, k)
        update_colors(r, g, b)
    except ValueError:
        pass

def on_cmyk_spinbox_change_for_bind(event):
    on_cmyk_spinbox_change()

def on_hsl_spinbox_change():
    try:
        h = int(h_spinbox.get())
        s = int(s_spinbox.get())
        l = int(l_spinbox.get())

        r, g, b = hsl_to_rgb(h, l, s)
        #hsl_label.set(h + ' ' + s + ' ' + l)
        update_colors(r,g,b)
    except ValueError:
        pass

def on_hsl_spinbox_change_for_bind(event):
    on_hsl_spinbox_change()
    

def on_slider_change(event):
    try:
        r = int(r_slider.get())
        g = int(g_slider.get())
        b = int(b_slider.get())
        update_colors(r,g,b)
    except ValueError:
        pass
# Создание основного окна
root = tk.Tk()
root.title("Color Converter")

# Элементы интерфейса
color_box = tk.Label(root, width=50, height=8)
color_box.pack(pady=10)
color_box.config(bg=f'#000000')

main_frame = tk.Frame(root)
main_frame.pack()
frame = tk.Frame(main_frame)
frame.grid(row=0,column=1)
tk.Label(frame, text="R:").grid(row=0, column=0)
r_spinbox = tk.Spinbox(frame, from_=0, to=255, increment=1, command=on_spinbox_change, width=3)
r_spinbox.grid(row=1, column=0)
#r_spinbox.grid(row=1, column=0)

tk.Label(frame, text="G:").grid(row=0, column=1)
g_spinbox = tk.Spinbox(frame, from_=0, to=255, increment=1, command=on_spinbox_change, width=3)
g_spinbox.grid(row=1, column=1)

tk.Label(frame, text="B:").grid(row=0, column=2)
b_spinbox = tk.Spinbox(frame, from_=0, to=255, increment=1, command=on_spinbox_change, width=3)
b_spinbox.grid(row=1, column=2)

#row=2
r_slider = tk.Scale(frame, from_=255, to=0, command=on_slider_change)
r_slider.grid(row=2, column=0)

g_slider = tk.Scale(frame, from_=255, to=0, command=on_slider_change)
g_slider.grid(row=2, column=1)

b_slider = tk.Scale(frame, from_=255, to=0, command=on_slider_change)
b_slider.grid(row=2, column=2)

# Кнопка выбора цвета
choose_color_button = tk.Button(root, text="Choose Color", command=choose_color)
choose_color_button.pack(pady=10)

# Подписи для CMYK и HSL
cmyk_label = tk.Label(root, text="CMYK: ")
cmyk_label.pack(pady=5)

hsl_label = tk.Label(root, text="HSL: ")
hsl_label.pack(pady=5)


# Связывание событий изменения текста в spinbox
r_spinbox.bind("<KeyRelease>", on_spinbox_change_for_bind)
g_spinbox.bind("<KeyRelease>", on_spinbox_change_for_bind)
b_spinbox.bind("<KeyRelease>", on_spinbox_change_for_bind)


#CMYK

cmyk_frame = tk.Frame(main_frame)
cmyk_frame.grid(row=0, column=0)

tk.Label(cmyk_frame, text="C:").grid(row=0, column=0)
tk.Label(cmyk_frame, text="M:").grid(row=0, column=1)
tk.Label(cmyk_frame, text="Y:").grid(row=0, column=2)
tk.Label(cmyk_frame, text="K:").grid(row=0, column=3)

#CMYK spinboxes
c_spinbox = tk.Spinbox(cmyk_frame, from_=0, to=100, increment=1, command=on_cmyk_spinbox_change)
c_spinbox.grid(row=1, column=0)

m_spinbox = tk.Spinbox(cmyk_frame, from_=0, to=100, increment=1, command=on_cmyk_spinbox_change)
m_spinbox.grid(row=1, column=1)

y_spinbox = tk.Spinbox(cmyk_frame, from_=0, to=100, increment=1, command=on_cmyk_spinbox_change)
y_spinbox.grid(row=1, column=2)

k_spinbox = tk.Spinbox(cmyk_frame, from_=0, to=100, increment=1, command=on_cmyk_spinbox_change)
k_spinbox.grid(row=1, column=3)

c_spinbox.bind("<KeyRelease>", on_cmyk_spinbox_change_for_bind)
m_spinbox.bind("<KeyRelease>", on_cmyk_spinbox_change_for_bind)
y_spinbox.bind("<KeyRelease>", on_cmyk_spinbox_change_for_bind)
k_spinbox.bind("<KeyRelease>", on_cmyk_spinbox_change_for_bind)

#HSL

hsl_frame = tk.Frame(main_frame)
hsl_frame.grid(row=0, column = 2)

tk.Label(hsl_frame, text="H:").grid(row=0, column=0)
tk.Label(hsl_frame, text="S:").grid(row=0, column=1)
tk.Label(hsl_frame, text="L:").grid(row=0, column=2)

#HSL spinboxes
h_spinbox = tk.Spinbox(hsl_frame, from_=0, to=360, increment=1, command=on_hsl_spinbox_change)
h_spinbox.grid(row=1, column=0)

s_spinbox = tk.Spinbox(hsl_frame, from_=0, to=100, increment=1, command=on_hsl_spinbox_change)
s_spinbox.grid(row=1, column=1)

l_spinbox = tk.Spinbox(hsl_frame, from_=0, to=100, increment=1, command=on_hsl_spinbox_change)
l_spinbox.grid(row=1, column=2)

h_spinbox.bind("<KeyRelease>", on_hsl_spinbox_change_for_bind)
s_spinbox.bind("<KeyRelease>", on_hsl_spinbox_change_for_bind)
l_spinbox.bind("<KeyRelease>", on_hsl_spinbox_change_for_bind)

# Запуск приложения
root.mainloop()