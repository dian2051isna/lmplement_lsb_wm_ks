import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def browse_image():
    path = filedialog.askopenfilename()
    if path:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            messagebox.showerror("Error", "Gambar tidak valid")
            return
        global original_image, image_path
        original_image = img
        image_path = path
        show_image(img)

def browse_watermark():
    path = filedialog.askopenfilename()
    if path:
        wm = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if wm is None:
            messagebox.showerror("Error", "Watermark tidak valid")
            return
        global watermark_image
        watermark_image = wm
        show_image(wm)

def embed_watermark():
    if original_image is None or watermark_image is None:
        messagebox.showerror("Error", "Pilih gambar dan watermark dulu!")
        return

    wm_resized = cv2.resize(watermark_image, (original_image.shape[1], original_image.shape[0]))

    # Proses penyisipan bit watermark ke dalam gambar asli
    watermarked = np.bitwise_and(original_image, 254)  # kosongkan bit LSB
    wm_bits = np.right_shift(wm_resized, 7)  # ambil bit MSB watermark (0 atau 1)
    result = np.bitwise_or(watermarked, wm_bits)

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")], title="Simpan gambar hasil")
    if save_path:
        cv2.imwrite(save_path, result)
        show_image(result)
        messagebox.showinfo("Berhasil", f"Watermark disisipkan ke {save_path}")

def show_image(img):
    # Tampilkan gambar di tkinter canvas
    img_pil = Image.fromarray(img)
    img_tk = ImageTk.PhotoImage(img_pil.resize((250, 250)))
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk

# Setup GUI
root = tk.Tk()
root.title("Watermark Steganografi (Grayscale)")

btn_browse_img = tk.Button(root, text="Pilih Gambar", command=browse_image)
btn_browse_img.pack(pady=5)

btn_browse_wm = tk.Button(root, text="Pilih Watermark", command=browse_watermark)
btn_browse_wm.pack(pady=5)

btn_embed = tk.Button(root, text="Sisipkan Watermark", command=embed_watermark)
btn_embed.pack(pady=10)

canvas = tk.Canvas(root, width=250, height=250, bg="gray")
canvas.pack(pady=10)

# Variabel global
original_image = None
watermark_image = None
image_path = ""

root.mainloop()