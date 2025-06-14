import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def load_and_extract():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if not file_path:
        return

    try:
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        wm_extracted = np.bitwise_and(img, 1) * 255  # Ekstrak LSB
        wm_extracted = Image.fromarray(np.uint8(wm_extracted))

        max_width, max_height = 250, 250
        wm_extracted.thumbnail((max_width, max_height))
        # wm_extracted.thumbnail((max_width, max_height), Image.ANTIALIAS)

        wm_img = ImageTk.PhotoImage(wm_extracted)
        wm_label.config(image=wm_img)
        wm_label.image = wm_img

        messagebox.showinfo("Sukses", "Watermark berhasil diekstrak!")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengekstrak watermark: {e}")

root = tk.Tk()
root.title("Ekstraksi Watermark (LSB)")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

btn_load = tk.Button(frame, text="Pilih Gambar dengan Watermark", command=load_and_extract)
btn_load.pack(pady=5)

wm_label = tk.Label(frame)
wm_label.pack(pady=10)

btn_save = tk.Button(frame, text="Simpan Hasil", command=lambda: wm_extracted.save("hasil_watermark.png"))
btn_save.pack(pady=5)

root.mainloop()
