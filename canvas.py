import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import math

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Imagem Rotacionando e Seguindo o Mouse")
        self.root.geometry("500x500")  # Define o tamanho da janela
        self.largura_janela = 500

        # Criar Canvas ocupando toda a janela
        self.canvas = tk.Canvas(root, bg="white", width=500, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Botão para carregar a imagem
        self.btn_carregar = tk.Button(root, text="Carregar Imagem", command=self.carregar_imagem)
        self.btn_carregar.pack()

        # Variáveis para armazenar a imagem carregada
        self.imagem_original = None
        self.imagem_tk = None
        self.imagem_id = None

        # Vincular evento de movimento do mouse ao canvas
        self.canvas.bind("<Motion>", self.mover_e_rotacionar_imagem)

    def carregar_imagem(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if not caminho:
            return

        # Carregar e redimensionar a imagem
        imagem = Image.open(caminho)
        largura_desejada = 250
        proporcao = largura_desejada / imagem.width
        nova_altura = int(imagem.height * proporcao)
        self.imagem_original = imagem.resize((largura_desejada, nova_altura), Image.LANCZOS)

        # Converter para formato do Tkinter
        self.imagem_tk = ImageTk.PhotoImage(self.imagem_original)

        # Se já houver uma imagem no canvas, remove antes de adicionar a nova
        if self.imagem_id:
            self.canvas.delete(self.imagem_id)

        # Criar imagem no canvas e armazenar seu ID
        self.imagem_id = self.canvas.create_image(250, 250, anchor=tk.CENTER, image=self.imagem_tk)

    def mover_e_rotacionar_imagem(self, event):
        """ Atualiza a posição e rotação da imagem de acordo com o movimento do mouse """
        if self.imagem_id and self.imagem_original:
            # Mover a imagem para seguir o mouse
            self.canvas.coords(self.imagem_id, event.x, event.y)

            # Calcular rotação proporcional à posição X do mouse
            angulo_rad = (event.x / self.largura_janela) * (2 * math.pi)  # De 0 a 2π rad
            angulo_graus = math.degrees(angulo_rad)

            # Rotacionar a imagem
            imagem_rotacionada = self.imagem_original.rotate(-angulo_graus, resample=Image.BICUBIC)

            # Converter para formato do Tkinter
            self.imagem_tk = ImageTk.PhotoImage(imagem_rotacionada)
            self.canvas.itemconfig(self.imagem_id, image=self.imagem_tk)

# Criar janela principal
root = tk.Tk()
app = App(root)
root.mainloop()