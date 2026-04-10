import tkinter as tk
from PIL import Image, ImageTk
import math

root = tk.Tk()
root.geometry("900x500")
root.title("Kettaga telefon")

valitud_number = ""

canvas = tk.Canvas(root, width=450, height=450)
canvas.place(relx=0, rely=0.5, anchor='w')

# Keskpunkt
cx, cy = 225, 225

### Piltide laadimine ja asetamine ###

# taust kõige alla
bg_img = Image.open("taust.png")
bg_tk = ImageTk.PhotoImage(bg_img)

bg_id = canvas.create_image(cx, cy, image=bg_tk)

# Numbrikihi lisamine liikumatu pilt
dial_img = Image.open("alus.png")
dial_tk = ImageTk.PhotoImage(dial_img)

dial_id = canvas.create_image(cx, cy, image=dial_tk)

# ketta kihi lisamine liikuv pilt
orig_img = Image.open("kettas.png")
current_img = orig_img
tk_img = ImageTk.PhotoImage(current_img)

image_id = canvas.create_image(cx+2, cy-3, image=tk_img)

# stopper ja pealmine lisa
stopper_img = Image.open("pealmine.png")
stopper_tk = ImageTk.PhotoImage(stopper_img)

stopper_id = canvas.create_image(cx, cy, image=stopper_tk)

# Seis
start_angle = None
current_angle = 0
dragging = False
valitud_sektor = None

# STOPPER (max pöördenurk)
global MAX_ANGLE
MAX_ANGLE = 270

def get_angle(x, y):
    dx = x - cx
    dy = cy - y
    angle = math.degrees(math.atan2(dy, dx))
    return (angle + 360) % 360


def angle_to_number(angle):
    sector = int(angle // 30)
    if 1 <= sector <= 9:
        return str(sector)
    elif sector == 10:
        return "0"
    return None


def on_press(event):
    global start_angle, dragging, valitud_sektor

    start_angle = get_angle(event.x, event.y)
    valitud_sektor = angle_to_number(start_angle)

    if valitud_sektor is not None:
        dragging = True


def on_drag(event):
    global current_angle, tk_img

    if not dragging:
        return

    angle = get_angle(event.x, event.y)
    delta = start_angle - angle  # oluline: ainult ühes suunas

    if delta < 0:
        delta = 0

    # piir stopperini
    delta = min(delta, MAX_ANGLE)

    current_angle = delta

    rotated = orig_img.rotate(-current_angle)
    tk_img = ImageTk.PhotoImage(rotated)
    canvas.itemconfig(image_id, image=tk_img)


def on_release(event):
    global dragging, valitud_number

    if not dragging:
        return

    dragging = False

    # registreeri number ainult siis kui piisavalt keeratud
    if current_angle > 20 and valitud_sektor:
        valitud_number += valitud_sektor
        print("Valitud:", valitud_number)

    tagasi_animatsioon()


def tagasi_animatsioon():
    global current_angle, tk_img

    if current_angle <= 0:
        return

    current_angle -= 5

    rotated = orig_img.rotate(-current_angle)
    tk_img = ImageTk.PhotoImage(rotated)
    canvas.itemconfig(image_id, image=tk_img)

    root.after(10, tagasi_animatsioon)


canvas.bind("<ButtonPress-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)

# Helistamis nupp
helistamine = tk.Button(root, text="Helista(sulgeb akna)", command=root.destroy)
helistamine.place(relx=0.9, rely=0.5, anchor='e')

root.mainloop()