import tkinter as tk
from datetime import datetime
import math

class RelogioAnalogico:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Relógio Analógico")
        self.janela.geometry("400x400")
        
        # Configurar canvas
        self.canvas = tk.Canvas(janela, width=400, height=400, bg='#e0f0ff')
        self.canvas.pack()
        
        # Coordenadas do centro e raio do relógio
        self.centro_x = 200
        self.centro_y = 200
        self.raio = 180
        
        # Criar elementos estáticos do relógio
        self._desenhar_mostrador()
        
        # Criar ponteiros
        self.ponteiro_horas = self.canvas.create_line(0, 0, 0, 0, width=6, fill='#2d2d2d', capstyle='round')
        self.ponteiro_minutos = self.canvas.create_line(0, 0, 0, 0, width=4, fill='#1e3f66', capstyle='round')
        self.ponteiro_segundos = self.canvas.create_line(0, 0, 0, 0, width=2, fill='#c00', capstyle='round')
        
        # Atualização inicial
        self.atualizar_relogio()

    def _desenhar_mostrador(self):
        # Desenhar borda decorativa
        self.canvas.create_oval(
            self.centro_x - self.raio,
            self.centro_y - self.raio,
            self.centro_x + self.raio,
            self.centro_y + self.raio,
            width=8,
            outline='#1e3f66'
        )
        
        # Desenhar marcações das horas
        for hora in range(12):
            angulo = math.radians(hora * 30 - 90)
            x_inicio = self.centro_x + (self.raio - 20) * math.cos(angulo)
            y_inicio = self.centro_y + (self.raio - 20) * math.sin(angulo)
            x_fim = self.centro_x + (self.raio - 8) * math.cos(angulo)
            y_fim = self.centro_y + (self.raio - 8) * math.sin(angulo)
            
            self.canvas.create_line(
                x_inicio, y_inicio,
                x_fim, y_fim,
                width=3,
                fill='#1e3f66'
            )
        
        # Desenhar números das horas
        for hora in range(12):
            angulo = math.radians(hora * 30 - 60)
            x = self.centro_x + (self.raio - 45) * math.cos(angulo)
            y = self.centro_y + (self.raio - 45) * math.sin(angulo)
            self.canvas.create_text(
                x, y,
                text=str(hora + 1),
                font=('Arial', 14, 'bold'),
                fill='#1e3f66'
            )
        
        # Desenhar centro do relógio
        self.canvas.create_oval(
            self.centro_x - 8,
            self.centro_y - 8,
            self.centro_x + 8,
            self.centro_y + 8,
            fill='#c00',
            outline='#2d2d2d'
        )

    def _calcular_posicao(self, angulo, comprimento):
        return (
            self.centro_x + comprimento * math.cos(angulo),
            self.centro_y + comprimento * math.sin(angulo)
        )

    def atualizar_relogio(self):
        agora = datetime.now()
        
        # Calcular ângulos
        segundos = agora.second
        minutos = agora.minute
        horas = agora.hour % 12
        
        angulo_segundos = math.radians(segundos * 6 - 90)
        angulo_minutos = math.radians((minutos * 6) + (segundos / 10) - 90)
        angulo_horas = math.radians((horas * 30) + (minutos / 2) - 90)
        
        # Atualizar posição dos ponteiros
        comprimentos = {
            'horas': self.raio * 0.5,
            'minutos': self.raio * 0.7,
            'segundos': self.raio * 0.8
        }
        
        # Atualizar ponteiro das horas
        x, y = self._calcular_posicao(angulo_horas, comprimentos['horas'])
        self.canvas.coords(self.ponteiro_horas, self.centro_x, self.centro_y, x, y)
        
        # Atualizar ponteiro dos minutos
        x, y = self._calcular_posicao(angulo_minutos, comprimentos['minutos'])
        self.canvas.coords(self.ponteiro_minutos, self.centro_x, self.centro_y, x, y)
        
        # Atualizar ponteiro dos segundos
        x, y = self._calcular_posicao(angulo_segundos, comprimentos['segundos'])
        self.canvas.coords(self.ponteiro_segundos, self.centro_x, self.centro_y, x, y)
        
        # Agendar próxima atualização
        self.janela.after(1000, self.atualizar_relogio)

if __name__ == "__main__":
    root = tk.Tk()
    relogio = RelogioAnalogico(root)
    root.mainloop()