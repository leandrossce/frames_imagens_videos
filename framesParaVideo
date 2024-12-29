import cv2
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_number(filename):
    match = re.match(r"(\d+)_", filename)
    if match:
        return int(match.group(1))
    return float('inf')

def select_image_directory():
    dir_path = filedialog.askdirectory(title="Selecione o diretório de imagens")
    if dir_path:
        img_dir_path_var.set(dir_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")], title="Selecione o arquivo de saída")
    if file_path:
        output_file_path_var.set(file_path)

def create_video():
    img_dir_path = img_dir_path_var.get()
    output_file_path = output_file_path_var.get()

    if not os.path.isdir(img_dir_path):
        messagebox.showerror("Erro", "Diretório de imagens inválido!")
        return

    if not output_file_path:
        messagebox.showerror("Erro", "Caminho do arquivo de saída inválido!")
        return

    try:
        # Get a list of all the image files in the directory, sorted by numeric order before "_"
        img_files = sorted(os.listdir(img_dir_path), key=extract_number)

        # Set the video codec and frame rate
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = 5

        # Get the dimensions of the first image
        img = cv2.imread(os.path.join(img_dir_path, img_files[0]))
        height, width, layers = img.shape

        # Create the VideoWriter object
        video = cv2.VideoWriter(output_file_path, fourcc, fps, (width, height))

        # Loop through each image file and add it to the video
        for img_file in img_files:
            img_path = os.path.join(img_dir_path, img_file)
            img = cv2.imread(img_path)
            print(img_path)
            video.write(img)

        # Release the VideoWriter object
        video.release()

        messagebox.showinfo("Sucesso", "Vídeo criado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao criar o vídeo: {e}")

# Create the main application window
root = tk.Tk()
root.title("Criador de Vídeo a partir de Imagens")

# Define Tkinter StringVar variables
img_dir_path_var = tk.StringVar()
output_file_path_var = tk.StringVar()

# Create and place widgets
tk.Label(root, text="Diretório de Imagens:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
img_dir_entry = tk.Entry(root, textvariable=img_dir_path_var, width=50)
img_dir_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Selecionar", command=select_image_directory).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Arquivo de Saída:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
output_file_entry = tk.Entry(root, textvariable=output_file_path_var, width=50)
output_file_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Selecionar", command=select_output_file).grid(row=1, column=2, padx=10, pady=5)

tk.Button(root, text="Criar Vídeo", command=create_video).grid(row=2, column=0, columnspan=3, pady=20)

# Run the application
root.mainloop()
