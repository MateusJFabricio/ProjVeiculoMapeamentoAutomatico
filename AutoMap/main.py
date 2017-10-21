
#controle do servo com os sensores

import RPi.GPIO as GPIO
import time
import serial
import turtle

#Configura a serial e a velocidade de transmissao
ser = serial.Serial("/dev/ttyS0", 115200, timeout=1)

PWM_MOTOR_IO = 22
TRIGGER_S1 = 17
ECHO_S1 = 27
TRIGGER_S2 = 18
ECHO_S2 = 23

class TMapa:
    def __init(self):
        turtle.Screen()
        turtle.speed(20)
        #turtle.hideturtle()

    def desenha(self, distancia, angulo):
        turtle.speed(20)
        turtle.penup()
        turtle.home()
        turtle.left(angulo)
        turtle.pendown()
        turtle.forward(distancia)
        
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
    
try:
    ser.close()
    ser.open()
    ser.flushInput()
    ser.flushOutput()
     
    servo = TServoMotor()
    sensor_dir = TSensorUSonico(TRIGGER_S1, ECHO_S1)
    sensor_esq = TSensorUSonico(TRIGGER_S2, ECHO_S2)

    mapa = TMapa()

    offset = 1
    
    while(0):
        for angulo in range(0,180,offset):
            servo.posicionar(180 - angulo)
            #print('No angulo' + str(servo.angulo))
            #print ('sensor da esqueda: '+ str(sensor_esq.medir()))
            #print ('sensor da direita: '+ str(sensor_dir.medir()))
            mapa.desenha(sensor_dir.medir(), servo.angulo)
            mapa.desenha(sensor_esq.medir(), servo.angulo + 180)
            
        for angulo in range(0,180,offset):
            servo.posicionar(angulo)
            #print('No angulo' + str(servo.angulo))
            #print ('   sensor da esqueda: '+ str(sensor_esq.medir()))
            #print ('   sensor da direita: '+ str(sensor_dir.medir()))
            mapa.desenha(sensor_dir.medir(), servo.angulo)
            mapa.desenha(sensor_esq.medir(), servo.angulo + 180)
            
        turtle.clearscreen()
        
finally:
    GPIO.cleanup()
    ser.close()
