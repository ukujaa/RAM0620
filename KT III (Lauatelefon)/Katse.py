import tkinter as tk
from PIL import Image, ImageTk
import math

root = tk.Tk()
root.geometry("900x500")

valitud_number = ""

# Pealkiri
root.title("Kettaga telefon")


def klikk(event):
    global valitud_number

    # keskpunkt (kohanda vastavalt pildile)
    center_x = 382/2
    center_y = 382/2

    dx = event.x - center_x
    dy = center_y - event.y

    angle = math.degrees(math.atan2(dy, dx))
    angle = (angle + 360) % 360  # 0–360

    # jagame 10 sektoriks (0–9)
    number = int(angle // 30)

    if number > 0 and number < 10:
        valitud_number += str(number)
    elif number == 10:
        valitud_number += "0"
    else:
        pass

    print("Valitud:", valitud_number)

# Helistamis nupp
helistamine = tk.Button(root, text="Helista(sulgeb akna)", command=root.destroy)
helistamine.place(relx=0.9, rely=0.5, anchor='e')

# Ketta importimine
pilt = Image.open('g11.png')
pilt = ImageTk.PhotoImage(pilt)

# Ketta kuvamine
image_label = tk.Label(root, image=pilt) # type: ignore
image_label.place(relx=0, rely=0.5, anchor='w')

# Seome kliki
image_label.bind("<Button-1>", klikk)

root.mainloop()