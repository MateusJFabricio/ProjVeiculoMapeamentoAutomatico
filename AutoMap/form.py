import turtle
import Tkinter as tk

def desenha(distancia, angulo, lousa):
    lousa.penup()
    lousa.home()
    lousa.left(angulo)
    lousa.pendown()
    lousa.forward(distancia)
        
def main():
    app = tk.Tk()
    app.title("Mapeamento 2D de ambiente ")
    app.fontePadrao = ("Arial", "10", "bold")
    
    app.primeiroContainer = tk.Frame(app)
    app.primeiroContainer["padx"] = 20
    app.primeiroContainer.pack()

    app.segundoContainer = tk.Frame(app)
    app.segundoContainer["padx"] = 20
    app.segundoContainer.pack()

    app.lblControle = tk.Label(app.primeiroContainer, text="Controle de movimento", font=app.fontePadrao)
    app.lblControle.pack(side=tk.TOP)

    app.frente = tk.Button(app.primeiroContainer)
    app.frente["text"] = "Frente"
    app.frente["font"] = ("Calibri", "8")
    app.frente["width"] = 12
    #app.frente["command"] = self.verificaSenha
    app.frente.pack()
    
    app.direita = tk.Button(app.primeiroContainer)
    app.direita["text"] = "Direita"
    app.direita["font"] = ("Calibri", "8")
    app.direita["width"] = 12
    #app.direita["command"] = self.verificaSenha
    app.direita.pack(side=tk.LEFT)

    app.esquerda = tk.Button(app.primeiroContainer)
    app.esquerda["text"] = "Esquerda"
    app.esquerda["font"] = ("Calibri", "8")
    app.esquerda["width"] = 12
    #app.esquerda["command"] = self.verificaSenha
    app.esquerda.pack(side=tk.RIGHT)

    app.re = tk.Button(app.primeiroContainer)
    app.re["text"] = "Re"
    app.re["font"] = ("Calibri", "8")
    app.re["width"] = 12
    #app.re["command"] = self.verificaSenha
    app.re.pack(side=tk.BOTTOM)
    
    app.lblCanvas = tk.Label(app.segundoContainer, text="Visualizacao do mapa", font=app.fontePadrao)
    app.lblCanvas.pack(side=tk.TOP)
    
    canvas = tk.Canvas(app.segundoContainer,width=500,height=500)
    canvas.pack()
    
    mapa = turtle.RawTurtle(canvas)
    for i in range(360):
       desenha(180, i,mapa)

    app.mainloop()

main()
