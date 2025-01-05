from PIL import Image
import os

# Função para recortar uma imagem a partir do centro
def crop_center(image, target_size):
    width, height = image.size
    new_width, new_height = target_size

    # Calcular coordenadas do centro
    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = (width + new_width) // 2
    bottom = (height + new_height) // 2

    # Retornar a imagem recortada
    return image.crop((left, top, right, bottom))

# Solicitar informações ao usuário
input_dir = input("Digite o caminho do diretório de entrada: ").strip()
output_dir = input("Digite o caminho do diretório de saída: ").strip()

# Solicitar dimensões do recorte
try:
    target_width = int(input("Digite a largura do recorte (em pixels): ").strip())
    target_height = int(input("Digite a altura do recorte (em pixels): ").strip())
    target_size = (target_width, target_height)
except ValueError:
    print("Erro: Por favor, insira valores numéricos válidos para as dimensões.")
    exit()

# Verificar se o diretório de saída existe, se não, criá-lo
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Listar os arquivos de imagem no diretório de entrada
image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpeg', '.jpg', '.png'))]

# Processar cada imagem
for image_file in image_files:
    try:
        # Abrir a imagem
        image_path = os.path.join(input_dir, image_file)
        image = Image.open(image_path)

        # Verificar se a imagem é menor que o tamanho desejado
        if image.size[0] < target_width or image.size[1] < target_height:
            print(f"Imagem {image_file} é menor que {target_width}x{target_height}, ignorada.")
            continue

        # Recortar a partir do centro
        cropped_image = crop_center(image, target_size)

        # Salvar a imagem recortada no diretório de saída
        output_path = os.path.join(output_dir, image_file)
        cropped_image.save(output_path)
        image.close()

        print(f"Imagem {image_file} processada com sucesso.")
    except Exception as e:
        print(f"Erro ao processar {image_file}: {e}")
