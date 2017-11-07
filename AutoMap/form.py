#controle do servo com os sensores

import RPi.GPIO as GPIO
import time
import serial
import turtle
from Tkinter import *
import canvasvg
import tkMessageBox

#Configura a serial e a velocidade de transmissao
ser = serial.Serial("/dev/ttyS0", 115200, timeout=1)

#Variaveis globais
#Controle Servo
PWM_MOTOR_IO = 22
#Controle dos sensores
TRIGGER_S1 = 17
ECHO_S1 = 27
TRIGGER_S2 = 18
ECHO_S2 = 23
#Controle motor tracao
RE_DIR_A = 24
RE_DIR_B = 25
RE_VEL = 19

RD_DIR_A = 5
RD_DIR_B = 6
RD_VEL = 13

#Inicializacao das portas
GPIO.setmode(GPIO.BCM)
#Inicializa a porta de direcao como Output
GPIO.setup(RE_DIR_A, GPIO.OUT)
GPIO.output(RE_DIR_A, 0)
GPIO.setup(RE_DIR_B, GPIO.OUT)
GPIO.output(RE_DIR_B, 0)

GPIO.setup(RD_DIR_A, GPIO.OUT)
GPIO.output(RD_DIR_A, 0)
GPIO.setup(RD_DIR_B, GPIO.OUT)
GPIO.output(RD_DIR_B, 0)
#Inicializa a porta de controle de velocidade
GPIO.setup(RE_VEL, GPIO.OUT)
RE_pwm = GPIO.PWM(RE_VEL, 100)

GPIO.setup(RD_VEL, GPIO.OUT)
RD_pwm = GPIO.PWM(RD_VEL, 100)

#Define a velocidade inicial do motor
RE_pwm.start(0)
RD_pwm.start(0)


class TServoMotor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PWM_MOTOR_IO, GPIO.OUT)
        self.pwm = GPIO.PWM(PWM_MOTOR_IO, 50)
        self.start()

    def posicionar(self, angulo):
        ser.write('A')
        print("Enviando " + str(angulo))
        ser.write(chr(angulo))
        print("Enviado - " + str(angulo))
        self.angulo = angulo

    def start(self):
        print("Instanciado Servo")

class TSensorUSonico:

    def __init__(self, trigger, echo):    
        self.trigger = trigger
        self.echo = echo
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.output(self.trigger, 0)
        GPIO.setup(self.echo, GPIO.IN)

    def medir(self):
        #Aciona o trigger
        GPIO.output(self.trigger, 1)
        time.sleep(0.00001)
        GPIO.output(self.trigger, 0)
        #inicia a contagem
        while GPIO.input(self.echo) == 0:
            start = time.time()
        #termina a contagem
        while GPIO.input(self.echo) == 1:
            stop = time.time()
        #calcula a distancia e retorna
        return (stop - start) * 17000
    

class Application:
    def __init__(self, master=None):
        #portas
        #######
        master.title("Mapeamento 2D de ambiente ")
        self.fontePadrao = ("Arial", "10", "bold")
        
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["padx"] = 20
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.lblControle = Label(self.primeiroContainer, text="Controle de movimento", font=self.fontePadrao)
        self.lblControle.pack(side=TOP)

        self.frente = Button(self.primeiroContainer)
        self.frente["text"] 		= "Frente"
        self.frente["font"] 		= ("Calibri", "8")
        self.frente["width"] 		= 12
        self.frente.bind("<Button-1>", self.cliqueBtnFrente)
        self.frente.bind("<ButtonRelease-1>", self.uncliqueBtnFrente)
        self.frente.pack()
        
        self.direita = Button(self.primeiroContainer)
        self.direita["text"] 		= "Direita"
        self.direita["font"] 		= ("Calibri", "8")
        self.direita["width"] 	= 12
        self.direita.bind("<Button-1>", self.cliqueBtnDireita)
        self.direita.bind("<ButtonRelease-1>", self.uncliqueBtnDireita)
        self.direita.pack(side=LEFT)

        self.esquerda = Button(self.primeiroContainer)
        self.esquerda["text"] 		= "Esquerda"
        self.esquerda["font"] 		= ("Calibri", "8")
        self.esquerda["width"] 		= 12
        self.esquerda.bind("<Button-1>", self.cliqueBtnEsquerda)
        self.esquerda.bind("<ButtonRelease-1>", self.uncliqueBtnEsquerda)
        self.esquerda.pack(side=RIGHT)

        self.re = Button(self.primeiroContainer)
        self.re["text"] 		= "Re"
        self.re["font"] 		= ("Calibri", "8")
        self.re["width"] 		= 12
        self.re.bind("<Button-1>", self.cliqueBtnRe)
        self.re.bind("<ButtonRelease-1>", self.uncliqueBtnRe)
        self.re.pack(side=BOTTOM)

        self.mapear = Button(self.terceiroContainer)
        self.mapear["text"] 		= "Mapear"
        self.mapear["font"] 		= ("Calibri", "8")
        self.mapear["width"] 		= 12
        self.mapear["command"] 	= self.cliqueMapear
        self.mapear.pack(side=LEFT)

        self.salvar = Button(self.terceiroContainer)
        self.salvar["text"] 		= "Salvar mapa"
        self.salvar["font"] 		= ("Calibri", "8")
        self.salvar["width"] 		= 12
        self.salvar.bind("<Button-1>", self.cliqueSalvar)
        self.salvar.pack(side=RIGHT)

        self.limpar = Button(self.terceiroContainer)
        self.limpar["text"] 		= "Limpar mapa"
        self.limpar["font"] 		= ("Calibri", "8")
        self.limpar["width"] 		= 12
        self.limpar["command"] 	= self.cliqueLimpar
        self.limpar.pack(side=RIGHT)

        self.inicio = Button(self.terceiroContainer)
        self.inicio["text"] 		= "Inicio"
        self.inicio["font"] 		= ("Calibri", "8")
        self.inicio["width"] 		= 12
        self.inicio["command"] 	= self.cliqueInicio
        self.inicio.pack(side=RIGHT)
        
        self.lblCanvas = Label(self.segundoContainer, text="Visualizacao do mapa", font=self.fontePadrao)
        self.lblCanvas.pack(side=TOP)
        
        self.canvas = Canvas(self.segundoContainer,width=500,height=500)
        self.canvas.pack()
        
        self.mapa = turtle.RawTurtle(self.canvas)

        self.meuAngulo = 0

    def cliqueBtnDireita(self, event):
        RD_pwm.ChangeDutyCycle(50)
        RE_pwm.ChangeDutyCycle(50)
        GPIO.output(RD_DIR_A, 0)
        GPIO.output(RD_DIR_B, 1)
        GPIO.output(RE_DIR_A, 0)
        GPIO.output(RE_DIR_B, 1)

    def uncliqueBtnDireita(self, event):
        RD_pwm.ChangeDutyCycle(0)
        RE_pwm.ChangeDutyCycle(0)
        GPIO.output(RD_DIR_A, 0)
        GPIO.output(RD_DIR_B, 0)
        GPIO.output(RE_DIR_A, 0)
        GPIO.output(RE_DIR_B, 0)

    def cliqueBtnEsquerda(self, event):
        RE_pwm.ChangeDutyCycle(50)
        RD_pwm.ChangeDutyCycle(50)
        GPIO.output(RE_DIR_A, 1)
        GPIO.output(RE_DIR_B, 0)
        GPIO.output(RD_DIR_A, 1)
        GPIO.output(RD_DIR_B, 0)

    def uncliqueBtnEsquerda(self, event):
        RE_pwm.ChangeDutyCycle(0)
        RD_pwm.ChangeDutyCycle(0)
        GPIO.output(RE_DIR_A, 0)
        GPIO.output(RE_DIR_B, 0)
        GPIO.output(RD_DIR_A, 0)
        GPIO.output(RD_DIR_B, 0)

    def cliqueBtnFrente(self, event):
        RE_pwm.ChangeDutyCycle(50)
        RD_pwm.ChangeDutyCycle(50)
        GPIO.output(RE_DIR_A, 1)
        GPIO.output(RE_DIR_B, 0)
        GPIO.output(RD_DIR_A, 0)
        GPIO.output(RD_DIR_B, 1)

    def uncliqueBtnFrente(self, event):
        RE_pwm.ChangeDutyCycle(0)
        RD_pwm.ChangeDutyCycle(0)
        GPIO.output(RE_DIR_A, 0)
        GPIO.output(RE_DIR_B, 0)
        GPIO.output(RD_DIR_A, 0)
        GPIO.output(RD_DIR_B, 0)

    def cliqueBtnRe(self, event):
        RE_pwm.ChangeDutyCycle(50)
        RD_pwm.ChangeDutyCycle(50)
        GPIO.output(RE_DIR_A, 0)
        GPIO.output(RE_DIR_B, 1)
        GPIO.output(RD_DIR_A, 1)
        GPIO.output(RD_DIR_B, 0)

    def uncliqueBtnRe(self, event):
        RE_pwm.ChangeDutyCycle(0)
        RD_pwm.ChangeDutyCycle(0)
        GPIO.output(RE_DIR_A, 0)
        GPIO.output(RE_DIR_B, 0)
        GPIO.output(RD_DIR_A, 0)
        GPIO.output(RD_DIR_B, 0) 

    def cliqueLimpar(self):
        self.mapa.clear()

    def cliqueInicio(self):
        self.mapa.penup()
        self.mapa.home()
        self.mapa.pendown()
        
    def cliqueSalvar(self, event):
        tkMessageBox.showinfo("Informacao","Verifique o terminal")
        self.nomeArquivo = raw_input("Digite o nome da imagem: ")
        self.ts = self.mapa.getscreen().getcanvas()
        canvasvg.saveall(self.nomeArquivo + ".svg", self.ts)
        tkMessageBox.showinfo("Informacao","Imagem ["+ self.nomeArquivo + ".svg]" +" salvo com sucesso!")
    
    def cliqueMapear(self):
        try:
            ser.close()
            ser.open()
            ser.flushInput()
            ser.flushOutput()
            
            self.servo = TServoMotor()
            self.sensor_dir = TSensorUSonico(TRIGGER_S1, ECHO_S1)
            self.sensor_esq = TSensorUSonico(TRIGGER_S2, ECHO_S2)

            self.offset = 1
            
            for angulo in range(0,180,self.offset):
                self.servo.posicionar(180 - angulo)
                self.desenha(self.sensor_dir.medir(), self.servo.angulo)
                self.desenha(self.sensor_esq.medir(), self.servo.angulo + 180)
                    
            for angulo in range(0,180, self.offset):
                self.servo.posicionar(angulo)
                self.desenha(self.sensor_dir.medir(), self.servo.angulo)
                self.desenha(self.sensor_esq.medir(), self.servo.angulo + 180)
                
        finally:
            ser.close()


    def desenha(self, distancia, angulo):
        self.mapa.speed(20)
        self.mapa.penup()
        self.mapa.home()
        self.mapa.left(angulo)
        self.mapa.pendown()
        self.mapa.forward(distancia)
      


root = Tk()
Application(root)
root.mainloop()
GPIO.cleanup()
