import random
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def novoNome():  # Função para gerar nomes aleatórios
    text = ""
    for i in range(22):
        text += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    return text

def selecionar_video():
    caminho_video = filedialog.askopenfilename(
        title="Selecione o arquivo de vídeo",
        filetypes=[("Arquivos MP4", "*.mp4")]
    )
    entrada_video.set(caminho_video)

def selecionar_diretorio():
    caminho_diretorio = filedialog.askdirectory(title="Selecione o diretório para salvar as imagens")
    saida_diretorio.set(caminho_diretorio)

def processar_video():
    video_path = entrada_video.get()
    output_dir = saida_diretorio.get()

    if not os.path.isfile(video_path):
        messagebox.showerror("Erro", "O caminho do vídeo não é válido.")
        return

    if not os.path.isdir(output_dir):
        messagebox.showerror("Erro", "O caminho do diretório não é válido.")
        return

    try:
        cap = cv2.VideoCapture(video_path)
        count = 0
        interval = 1  # Intervalo para salvar frames

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if count % interval == 0:
                # Cortar a imagem para 512x512 pixels
                height, width, _ = frame.shape
                min_dim = min(height, width)
                start_x = (width - min_dim) // 2
                start_y = (height - min_dim) // 2
                cropped_frame = frame[start_y:start_y + min_dim, start_x:start_x + min_dim]
                resized_frame = cv2.resize(cropped_frame, (512, 512))

                filename = os.path.join(output_dir, f"{count}_frame.jpg")
                cv2.imwrite(filename, resized_frame)
                print(f"Frame salvo: {filename}")

            count += 1

        cap.release()
        messagebox.showinfo("Concluído", "Processamento do vídeo concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o processamento: {e}")

# Interface Gráfica com Tkinter
root = tk.Tk()
root.title("Extrator de Frames de Vídeo")

entrada_video = tk.StringVar()
saida_diretorio = tk.StringVar()

# Seção para selecionar o vídeo
tk.Label(root, text="Caminho do vídeo (.mp4):").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_video = tk.Entry(root, textvariable=entrada_video, width=50)
entry_video.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Selecionar", command=selecionar_video).grid(row=0, column=2, padx=10, pady=10)

# Seção para selecionar o diretório de saída
tk.Label(root, text="Diretório de saída:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_diretorio = tk.Entry(root, textvariable=saida_diretorio, width=50)
entry_diretorio.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Selecionar", command=selecionar_diretorio).grid(row=1, column=2, padx=10, pady=10)

# Botão para iniciar o processamento
tk.Button(root, text="Iniciar Processamento", command=processar_video, bg="green", fg="white").grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
