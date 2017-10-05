#L293D
#Controle motor Dc utilizando CI L293D

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

DIR_A = 5
DIR_B = 6
VEL = 13

#Inicializa a porta de direção como Output
GPIO.setup(DIR_A, GPIO.OUT)
GPIO.output(DIR_A, 0)

GPIO.setup(DIR_B, GPIO.OUT)
GPIO.output(DIR_B, 0)

#Inicializa a porta de controle de velocidade
GPIO.setup(VEL, GPIO.OUT)
pwm = GPIO.PWM(VEL, 100)

#Define a velocidade do motor
#A velocidade de 0% até 100%
#Neste caso esta com 50%
pwm.start(50)

#Define a direção do motor
#Para inverter, basta desabilitar uma saida e habilitar a outra
GPIO.output(DIR_A, 1)
GPIO.output(DIR_A, 0)

#Para para o motor, basta desabilitar o controle de direção, ou zerar a velocidade.
#Para este exemplo, eu adicionei um cleanup, somente para teste

time.sleep(3)

GPIO.cleanup()
