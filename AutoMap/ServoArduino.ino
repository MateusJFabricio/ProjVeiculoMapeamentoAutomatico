#include <Servo.h> 
Servo servo;

const int pino_led = 13;
char buf;
int angulo = 90; 
 
void setup()
{
  servo.attach(8);
  servo.write(90);
  Serial.begin(9600);
}
 
void loop()
{
  while (Serial.available() > 0)
  {
    angulo = Serial.read();
    servo.write(angulo);
  }
}
