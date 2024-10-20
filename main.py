import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageOps, ImageTk
import os

def convert_glossiness_to_roughness(input_path, output_path):
    try:
        # Open the image
        image = Image.open(input_path).convert('L')  # Convert to grayscale

        # Invert the image to convert glossiness to roughness
        roughness_image = ImageOps.invert(image)

        # Save the image
        roughness_image.save(output_path)
        messagebox.showinfo("Succès", f"Conversion done : {output_path}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Error while converting : {e}")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        update_image(file_path)

def update_image(file_path):
    global img
    img = Image.open(file_path)
    img.thumbnail((256, 256))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk
    image_label.image_path = file_path

    # Set output path
    base, ext = os.path.splitext(file_path)
    base = base.replace("_gloss", "").replace("_glossiness", "")
    output_path = base + "_roughness" + ext
    output_path_var.set(output_path)

def on_drop(event):
    file_path = event.data.strip('{}')  # Remove curly braces
    update_image(file_path)

def convert():
    input_path = image_label.image_path
    output_path = output_path_var.get()
    if input_path and output_path:
        convert_glossiness_to_roughness(input_path, output_path)

# Set up the GUI
root = TkinterDnD.Tk()
root.title("Source 2 Glossiness to Roughness Converter")
root.geometry("400x400")
root.resizable(False, False)

root.iconbitmap('icon.ico')

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Image display
image_label = tk.Label(frame, text="Drop an image here", width=256, height=256, relief="solid")
image_label.pack(pady=5)
image_label.drop_target_register(DND_FILES)
image_label.dnd_bind('<<Drop>>', on_drop)
image_label.bind("<Button-1>", lambda e: open_file())

# Output path
output_path_var = tk.StringVar()
output_entry = tk.Entry(frame, textvariable=output_path_var, width=50)
output_entry.pack(pady=5)

def choose_output_directory():
    directory = filedialog.askdirectory()
    if directory:
        base_name = os.path.basename(output_path_var.get())
        output_path_var.set(os.path.join(directory, base_name))

choose_dir_button = tk.Button(frame, text="Choose folder", command=choose_output_directory)
choose_dir_button.pack(pady=5)

# Convert button
convert_button = tk.Button(frame, text="Convert", command=convert)
convert_button.pack(pady=5)

root.mainloop()