import math
import tkinter as tk
from tkinter import Button, Entry, Canvas, PhotoImage


class MainApplication(tk.Frame):
    """Classe da Aplicacao"""

    point_button_type = 0 #botoes de adquirir os pontos
    x_point1 = y_point1 = 0
    x_point2 = y_point2 = 0

    def __init__(self, parent, *args, **kwargs):
        """Construtor da classe"""

        global px,py
        tk.PanedWindow.__init__(self, parent, *args, **kwargs)
        self.window = parent
        self.define_window_properties()
        self.create_button_panel()
        self.create_paint_screen()

    def define_window_properties(self):
        """"Definindo propriedades da janela"""

        self.window.title('Computacao Grafica')
        self.window.minsize(500, 500)

    def create_button_panel(self):
        """Cria o painel lateral onde ficam alocados os botoes"""

        self.button_frame = tk.Frame(self.window, bg='#2c3e50')
        self.button_frame.pack(side='left', fill='both')

        self.entry1 = Entry(self.button_frame)
        self.entry1.insert(0, '(0, 0)')
        self.entry1.config(state='readonly')
        self.entry1.pack(padx=5, pady=15)
        self.entry2 = Entry(self.button_frame)
        self.entry2.insert(0, '(0, 0)')
        self.entry2.config(state='readonly')
        self.entry2.pack(padx=5)

        self.b_point1 = Button(self.button_frame, text='Set Point 1',
                               command=self.set_point1)
        self.b_point1.pack(padx=10, pady=10, fill='x')
        self.b_point2 = Button(self.button_frame, text='Set Point 2',
                               command=self.set_point2)
        self.b_point2.pack(padx=10, pady=5, fill='x')

        separator = tk.Frame(self.button_frame,
                             relief='ridge', height=2, bg="#7f8c8d")
        separator.pack(pady=5, fill='x')

        self.b_dda = Button(self.button_frame, text='DDA',
                               command=self.DDA_algorithm)
        self.b_dda.pack(padx=10, pady=5, fill='x')
        self.b_circle = Button(self.button_frame, text='Circulo',
                               command=self.midpoint_circle_algoritm)
        self.b_circle.pack(padx=10, pady=10, fill='x')
        self.b_clear = Button(self.button_frame, text='Clear',
                               command=self.clear_canvas)
        self.b_clear.pack(padx=10, pady=5, fill='x')

    def create_paint_screen(self):
        """Cria o canvas e a imagem usada para pintar pixels na tela"""

        self.canvas = Canvas(self.window, background='#bdc3c7')
        self.canvas.pack(side='left', fill='both', expand=1)
        self.canvas.bind('<Configure>', self.on_resize)
        self.img = PhotoImage()
        self.img_reference = self.canvas.create_image((0, 0), image=self.img,
                                 state="normal", anchor="nw")
        self.canvas.focus_set()
        self.canvas.tag_bind(self.img_reference,
                             '<Button-1>', self.on_img_click)

    def on_img_click(self, event):
        """Metodo de resposta ao clique no canvas"""

        if(self.point_button_type != 0):
            b_type = self.point_button_type
            color = '#ff0000' if b_type == 1 else '#ff0066'
            entry_ref = self.entry1 if b_type == 1 else self.entry2

            if(b_type == 1):
                self.x_point1 = event.x
                self.y_point1 = event.y
            else:
                self.x_point2 = event.x
                self.y_point2 = event.y

            self.paint_point(event.x, event.y, color)
            entry_ref.config(state='normal')
            entry_ref.delete(0,'end')
            entry_ref.insert(0, '(' + str(event.x) + ' , '+str(event.y) + ')')
            entry_ref.config(state='readonly')

        self.point_button_type = 0

    def on_resize(self, event):
        """Metodo de resposta ao ajuste do tamanho da janela"""
        c_width = event.width
        c_height = event.height
        self.img.config(width=c_width, height=c_height)

    def set_point1(self):
        """Setando que o botao de selecionar o ponto 1 foi clickado"""

        self.point_button_type = 1

    def set_point2(self):
        """Setando que o botao de selecionar o ponto 2 foi clickado"""

        self.point_button_type = 2

    def paint_point(self, x, y, color):
        """"Metodo para pintar um quadrado ao redor do ponto selecionado"""

        if(x > 0 and y > 0):
            self.paint_pixel(x-1, y-1, color)
        if(x > 0):
            self.paint_pixel(x-1, y, color)
            self.paint_pixel(x-1, y+1, color)
        if(y>0):
            self.paint_pixel(x, y-1, color)
            self.paint_pixel(x+1, y-1, color)

        self.paint_pixel(x, y, color)
        self.paint_pixel(x, y+1, color)
        self.paint_pixel(x+1, y, color)
        self.paint_pixel(x+1, y+1, color)

    def paint_pixel(self, x, y, color):
        """Metodo que pinta um pixel no canvas"""

        self.img.put(color, (x, y))

    def clear_canvas(self):
        """Metodo que limpa o canvas (destruindo e recriando-o)"""
        self.canvas.destroy()
        self.create_paint_screen()

    def DDA_algorithm(self):
        """Metodo Digital Differential Analyzer (DDA) para exibir de retas"""

        delta_x = self.x_point2 - self.x_point1
        delta_y = self.y_point2 - self.y_point1
        coef_ang = 0

        if(delta_x != 0) :
            coef_ang = delta_y/delta_x

        self.paint_pixel(self.x_point1, self.y_point1, '#000000')

        if(coef_ang <= 1):
            float_value = self.y_point1

            for i in range(self.x_point1+1, self.x_point2+1):
                self.paint_pixel(i, int(float_value), '#000000')
                float_value += coef_ang
        else:
            float_value = self.x_point1

            for i in range(self.y_point1+1, self.y_point2+1):
                float_value += (1/coef_ang)
                self.paint_pixel(int(float_value), i, '#000000')

    def midpoint_circle_algoritm(self):
        """"Metodo de rasterizacao de circulos"""

        delta_x = self.x_point2 - self.x_point1
        delta_y = self.y_point2 - self.y_point1
        radius = math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))

        x = radius - 1
        y = 0
        dx = 1
        dy = 1
        err = dx - (radius * 2)

        while (x >= y):
            self.paint_pixel(int(self.x_point1 + x), int(self.y_point1 + y), '#000000');
            self.paint_pixel(int(self.x_point1 + y), int(self.y_point1 + x), '#000000');
            self.paint_pixel(int(self.x_point1 - y), int(self.y_point1 + x), '#000000');
            self.paint_pixel(int(self.x_point1 - x), int(self.y_point1 + y), '#000000');
            self.paint_pixel(int(self.x_point1 - x), int(self.y_point1 - y), '#000000');
            self.paint_pixel(int(self.x_point1 - y), int(self.y_point1 - x), '#000000');
            self.paint_pixel(int(self.x_point1 + y), int(self.y_point1 - x), '#000000');
            self.paint_pixel(int(self.x_point1 + x), int(self.y_point1 - y), '#000000');

            if (err <= 0):
                y += 1
                err += dy
                dy += 2
            if (err > 0):
                x -= 1
                dx += 2
                err += (-radius * 2) + dx

# Executando a classe
if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()
