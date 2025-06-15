import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

wm_extracted_img = None 

def load_and_extract():
    global wm_extracted_img 
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if not file_path:
        return

    try:
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        wm = np.bitwise_and(img, 1) * 255 
        wm_extracted_img = Image.fromarray(np.uint8(wm))

        max_width, max_height = 250, 250
        wm_extracted_img.thumbnail((max_width, max_height))

        wm_img = ImageTk.PhotoImage(wm_extracted_img)
        wm_label.config(image=wm_img)
        wm_label.image = wm_img

        messagebox.showinfo("Sukses", "Watermark berhasil diekstrak!")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengekstrak watermark: {e}")

def save_result():
    if wm_extracted_img:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            wm_extracted_img.save(save_path)
            messagebox.showinfo("Sukses", "Pengecekan berhasil dan watermark/gambar tersembunyi berhasil disimpan.")
    else:
        messagebox.showwarning("Belum Ada Gambar", "Belum ada gambar hasil untuk disimpan.")

root = tk.Tk()
root.title("Ekstraksi Watermark (LSB)")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

btn_load = tk.Button(frame, text="Pilih Gambar dengan Watermark", command=load_and_extract)
btn_load.pack(pady=5)

wm_label = tk.Label(frame)
wm_label.pack(pady=10)

btn_save = tk.Button(frame, text="Simpan Hasil", command=save_result)
btn_save.pack(pady=5)

root.mainloop()
