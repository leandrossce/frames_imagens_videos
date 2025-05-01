import os
import cv2
import numpy as np
from rembg import remove
from PIL import Image
import tkinter as tk
from tkinter import filedialog

# Força o uso apenas da CPU no ONNX Runtime
os.environ["ORT_DISABLE_ALL_OPTIMIZATIONS"] = "1"

def selecionar_diretorio(mensagem):
    """ Abre uma janela para o usuário selecionar um diretório. """
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=mensagem)

def remover_fundo(imagem_pil):
    """ Remove o fundo da imagem usando rembg. """
    return remove(imagem_pil)

def recortar_para_objeto(imagem_pil, margem=10):
    """ 
    Recorta a imagem para remover todas as áreas transparentes ao redor do objeto.
    A margem adiciona uma borda para evitar cortes muito justos.
    """
    imagem_cv = np.array(imagem_pil)

    # Verifica se a imagem tem canal Alpha (transparência)
    if imagem_cv.shape[-1] == 4:
        mask = imagem_cv[:, :, 3]  # Usa o canal Alpha como máscara
    else:
        mask = cv2.cvtColor(imagem_cv, cv2.COLOR_RGB2GRAY)  # Converte para escala de cinza

    # Criar uma máscara binária onde o objeto é branco e o fundo é preto
    _, thresh = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

    # Encontrar todos os contornos na máscara
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contornos:
        # Encontrar o maior contorno (o objeto principal)
        maior_contorno = max(contornos, key=cv2.contourArea)

        # Determinar um retângulo ao redor do objeto principal
        x, y, w, h = cv2.boundingRect(maior_contorno)

        # Adicionar uma margem ao redor do objeto (evita cortes muito justos)
        x = max(x - margem, 0)
        y = max(y - margem, 0)
        w = min(w + 2 * margem, imagem_pil.width - x)
        h = min(h + 2 * margem, imagem_pil.height - y)

        # Recortar a imagem na área do objeto detectado
        return imagem_pil.crop((x, y, x + w, y + h))

    return imagem_pil  # Retorna a imagem original caso não haja contornos detectados

def preencher_fundo_transparente(imagem_pil, cor=(255, 255, 255)):
    """ Se for salvar em JPEG, substitui a transparência pelo fundo branco. """
    if imagem_pil.mode == "RGBA":
        nova_imagem = Image.new("RGB", imagem_pil.size, cor)
        nova_imagem.paste(imagem_pil, mask=imagem_pil.split()[3])  # Usa a transparência como máscara
        return nova_imagem
    return imagem_pil

def processar_diretorio(input_dir, output_dir, formato="png"):
    """ Processa todas as imagens do diretório, remove o fundo e recorta o objeto visível. """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for arquivo in os.listdir(input_dir):
        caminho_entrada = os.path.join(input_dir, arquivo)

        if arquivo.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".webp")):
            try:
                imagem = Image.open(caminho_entrada)
                imagem_sem_fundo = remover_fundo(imagem)
                imagem_recortada = recortar_para_objeto(imagem_sem_fundo, margem=20)  # Recorta apenas o objeto visível

                # Garante que a imagem não fique com dimensões muito pequenas
                if imagem_recortada.width < 30 or imagem_recortada.height < 30:
                    print(f"⚠️ Atenção: A imagem {arquivo} ficou muito pequena após o recorte e pode estar incorreta.")

                # Configuração do formato de saída
                nome_saida, ext = os.path.splitext(arquivo)
                if formato == "png":
                    caminho_saida = os.path.join(output_dir, f"{nome_saida}.png")
                    imagem_recortada.save(caminho_saida, "PNG")
                else:
                    caminho_saida = os.path.join(output_dir, f"{nome_saida}.jpg")
                    imagem_jpeg = preencher_fundo_transparente(imagem_recortada)  # Substitui transparência por branco
                    imagem_jpeg.save(caminho_saida, "JPEG", quality=95)

                print(f"✅ Processado: {arquivo}")
            except Exception as e:
                print(f"❌ Erro ao processar {arquivo}: {e}")

# Seleção de diretórios
input_directory = selecionar_diretorio("Selecione o diretório com as imagens")
output_directory = selecionar_diretorio("Selecione o diretório para salvar as imagens recortadas")

if input_directory and output_directory:
    processar_diretorio(input_directory, output_directory, formato="png")  # Troque para "jpg" se quiser JPEG
    print("\n🚀 Processamento concluído! As imagens finais contêm apenas o objeto visível.")
else:
    print("\n❌ Operação cancelada.")
