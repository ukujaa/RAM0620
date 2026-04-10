import tkinter as tk
from tkinter import *
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

### Pildid ###

bg_img = Image.open("taust.png")
bg_tk = ImageTk.PhotoImage(bg_img)
canvas.bg = bg_tk
bg_id = canvas.create_image(cx, cy, image=bg_tk)

dial_img = Image.open("alus.png")
dial_tk = ImageTk.PhotoImage(dial_img)
canvas.dial = dial_tk
dial_id = canvas.create_image(cx, cy, image=dial_tk)

orig_img = Image.open("kettas.png")
tk_img = ImageTk.PhotoImage(orig_img)
canvas.wheel = tk_img
image_id = canvas.create_image(cx+2, cy-3, image=tk_img)

stopper_img = Image.open("pealmine.png")
stopper_tk = ImageTk.PhotoImage(stopper_img)
canvas.stopper = stopper_tk
stopper_id = canvas.create_image(cx, cy, image=stopper_tk)

### Seis ###
start_angle = None
current_angle = 0
dragging = False
valitud_sektor = None

STOPPER_ANGLE = 0  # muuda kui vaja (nt 90 kui stopper on üleval)

numbri_kuvamine = tk.Label(root, text="", font=("Arial", 16, "bold"), relief="groove")
numbri_kuvamine.place(relx=0.9, rely=0.3, anchor='ne')

### Funktsioonid ###

def tee_nupp():
    numbri_kuvamine = tk.Label(root, text=valitud_number, font=("Arial", 16, "bold"), relief="groove")
    numbri_kuvamine.place(relx=0.9, rely=0.3, anchor='ne')

def helista():
    root.withdraw()
    toplevel = Toplevel(root)
    toplevel.title("Kõne")
    numbri_kuvamine = tk.Label(toplevel, bg="light blue" , text="Mobiiltelefon, millele te helistate\nei ole sisse lülitatud või\nasub väljaspool võrgu teeninduspiirkonda", font=("Arial", 16, "bold"), relief="groove")
    numbri_kuvamine.pack()

    toplevel.protocol("WM_DELETE_WINDOW", root.destroy)
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


def number_to_angle(number):
    if number == "0":
        sector = 10
    else:
        sector = int(number)
    return sector * 30


def on_press(event):
    global start_angle, dragging, valitud_sektor

    start_angle = get_angle(event.x, event.y)
    valitud_sektor = angle_to_number(start_angle)

    if valitud_sektor:
        dragging = True


def on_drag(event):
    global current_angle, tk_img

    if not dragging or not valitud_sektor:
        return

    mouse_angle = get_angle(event.x, event.y)

    number_angle = number_to_angle(valitud_sektor)

    # kui palju peab pöörama stopperini
    target_rotation = (number_angle - STOPPER_ANGLE) % 360

    # kui palju kasutaja on tõmmanud
    dragged = (start_angle - mouse_angle) % 360

    # ei lase üle stopperi
    current_angle = min(dragged, target_rotation)

    rotated = orig_img.rotate(-current_angle)
    tk_img = ImageTk.PhotoImage(rotated)
    canvas.itemconfig(image_id, image=tk_img)
    canvas.wheel = tk_img


def on_release(event):
    global dragging, valitud_number

    if not dragging:
        return

    dragging = False

    number_angle = number_to_angle(valitud_sektor)
    target_rotation = (number_angle - STOPPER_ANGLE) % 360

    # ainult kui jõudis stopperini
    if abs(current_angle - target_rotation) < 10:
        valitud_number += valitud_sektor

        # visualiseerime oma telefoninumbri
        tee_nupp()

    tagasi_animatsioon()


def tagasi_animatsioon():
    global current_angle, tk_img

    if current_angle <= 0:
        return

    current_angle -= 5

    rotated = orig_img.rotate(-current_angle)
    tk_img = ImageTk.PhotoImage(rotated)
    canvas.itemconfig(image_id, image=tk_img)
    canvas.wheel = tk_img

    root.after(10, tagasi_animatsioon)


### Eventid ###
canvas.bind("<ButtonPress-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)


# Nupp
helistamine = tk.Button(root, text="Helista valitud numbril",font="16", command=helista)
helistamine.place(relx=0.9, rely=0.5, anchor='e')

#numbri_kuvamine = tk.Label(root, text=5080265,font=("Arial", 16, "bold"), relief="groove")
#numbri_kuvamine.place(relx=0.9, rely=0.3, anchor='ne')

root.mainloop()