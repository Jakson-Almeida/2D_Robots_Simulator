import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Imagem Seguindo o Mouse")
        self.root.geometry("500x500")  # Define o tamanho da janela
        
        # Criar Canvas ocupando toda a janela
        self.canvas = tk.Canvas(root, bg="white", width=500, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Botão para carregar a imagem
        self.btn_carregar = tk.Button(root, text="Carregar Imagem", command=self.carregar_imagem)
        self.btn_carregar.pack()

        # Variável para armazenar a imagem carregada
        self.imagem_tk = None
        self.imagem_id = None

        # Vincular evento de movimento do mouse ao canvas
        self.canvas.bind("<Motion>", self.mover_imagem)

    def carregar_imagem(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if not caminho:
            return

        # Carregar e redimensionar a imagem
        imagem = Image.open(caminho)
        largura_desejada = 250
        proporcao = largura_desejada / imagem.width
        nova_altura = int(imagem.height * proporcao)
        imagem = imagem.resize((largura_desejada, nova_altura), Image.LANCZOS)

        # Converter para formato do Tkinter
        self.imagem_tk = ImageTk.PhotoImage(imagem)

        # Se já houver uma imagem no canvas, remove antes de adicionar a nova
        if self.imagem_id:
            self.canvas.delete(self.imagem_id)

        # Criar imagem no canvas e armazenar seu ID
        self.imagem_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imagem_tk)

    def mover_imagem(self, event):
        """ Atualiza a posição da imagem para seguir o mouse """
        if self.imagem_id:
            self.canvas.coords(self.imagem_id, event.x, event.y)

# Criar janela principal
root = tk.Tk()
app = App(root)
root.mainloop()