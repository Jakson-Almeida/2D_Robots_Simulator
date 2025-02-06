import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Função para carregar e exibir a imagem no Canvas
def carregar_imagem():
    caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if not caminho:
        return

    # Carregar a imagem com Pillow
    imagem = Image.open(caminho)

    # Redimensionar mantendo a proporção
    largura_desejada = 250
    proporcao = largura_desejada / imagem.width
    nova_altura = int(imagem.height * proporcao)
    imagem = imagem.resize((largura_desejada, nova_altura), Image.LANCZOS)

    # Converter para formato do Tkinter
    imagem_tk = ImageTk.PhotoImage(imagem)

    # Atualizar o Canvas
    canvas.config(width=largura_desejada, height=nova_altura)
    canvas.create_image(0, 0, anchor=tk.NW, image=imagem_tk)
    canvas.image = imagem_tk  # Manter referência para evitar garbage collection

# Criar janela principal
root = tk.Tk()
root.title("Exibir Imagem no Canvas")

# Criar Canvas
canvas = tk.Canvas(root, bg="white")
canvas.pack()

# Botão para carregar imagem
btn_carregar = tk.Button(root, text="Carregar Imagem", command=carregar_imagem)
btn_carregar.pack()

# Iniciar loop do Tkinter
root.mainloop()