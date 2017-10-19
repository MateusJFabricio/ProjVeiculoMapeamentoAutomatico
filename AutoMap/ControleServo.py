import RPi.GPIO as GPIO
import time
import serial
 
#Configura a serial e a velocidade de transmissao
ser = serial.Serial("/dev/ttyS0", 9600, timeout=1)

#GPIO.setmode(GPIO.BOARD)
 
#Define o pino do botao como entrada
#GPIO.setup(18, GPIO.IN)
 
#Mensagem inicial
#print ("Pressione o botao...")

try:
     ser.close()
     ser.open()
     ser.flushInput()
     ser.flushOutput()
     while(1):
          for a in range(180):
               ser.write('A')
               print("Enviando " + str(a))
               ser.write(chr(a))
               print("Enviado - " + str(a))
               #time.sleep(0.05)
               
          for a in range(180):
               ser.write('A')
               print("Enviando " + str(180 - a))
               ser.write(chr(180 - a))
               print("Enviado - " + str(180 - a))
               #time.sleep(0.05)
          
except:
     print("passei no excep")
     ser.close()
     raise
