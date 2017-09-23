#controle do servo com os sensores

import RPi.GPIO as GPIO
import time

PWM_MOTOR_IO = 22
TRIGGER_S1 = 17
ECHO_S1 = 27
TRIGGER_S2 = 18
ECHO_S2 = 23



class TServoMotor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PWM_MOTOR_IO, GPIO.OUT)
        self.pwm = GPIO.PWM(PWM_MOTOR_IO, 50)
        self.start()

    def posicionar(self, angulo):
        duty = float(angulo) * 0.0333 + 4.5
        print('O valor do duty: ' + str(duty))
        if not (self.angulo == angulo):
            self.pwm.ChangeDutyCycle(duty)
            time.sleep(0.1)
        #self.pwm.stop()
        self.angulo = angulo

    def start(self):
        self.pwm.start(4.5)
        self.angulo = 0

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
    servo = TServoMotor()
    sensor_dir = TSensorUSonico(TRIGGER_S1, ECHO_S1)
    sensor_esq = TSensorUSonico(TRIGGER_S2, ECHO_S2)

    offset = 4
    while(True):
        for angulo in range(0,180,offset):
            servo.posicionar(180 - angulo)
            time.sleep(0.1)
            print('No angulo' + str(servo.angulo))
            print ('sensor da esqueda: '+ str(sensor_esq.medir()))
            print ('sensor da direita: '+ str(sensor_dir.medir()))

        for angulo in range(0,180,offset):
            servo.posicionar(angulo)
            time.sleep(0.1)
            print('No angulo' + str(servo.angulo))
            print ('   sensor da esqueda: '+ str(sensor_esq.medir()))
            print ('   sensor da direita: '+ str(sensor_dir.medir()))
        
finally:
    GPIO.cleanup()

