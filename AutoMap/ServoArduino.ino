//Programa : Teste MPU6050 e LCD 20x4
//Alteracoes e adaptacoes : FILIPEFLOP
//
//Baseado no programa original de JohnChi

//Carrega a biblioteca Wire
#include<Wire.h>
#include <Servo.h> 


//Endereco I2C do MPU6050
const int MPU=0x68;  

//Instancia Servo
Servo servo;

char buf;
int angulo = 90; 
String Bussola;
char valorSerial;

//Variaveis para armazenar valores dos sensores
int AnguloX, AnguloY, AnguloZ;
void setup()
{
  Serial.begin(115200);
  Serial.flush();

  //Inicializa o servo motor
  servo.attach(8);

  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B); 
  
  //Inicializa o MPU-6050
  Wire.write(0); 
  Wire.endTransmission(true);
}
void serialEvent(){
  char temp;
  temp = Serial.read();
  Serial.println(temp);
  if (valorSerial == 'A'){
    angulo = (byte) temp;
    valorSerial = 'c';
  }else{
    valorSerial = temp;
  }
  
}
void loop()
{
  if (angulo >= 0){
      servo.write(angulo);
      Serial.print((int)angulo);
      angulo = -1;
  }
  /*
  if(buf = 'B'){
    Bussola = LerBussola();
    //Envia por serial os valores da bussola
    for (int i = 0; i < Bussola.length(); i++)
    {
      Serial.write(Bussola[i]);
    }
    
    }
  }
  */
 }

 String LerBussola()
 {
   //Ainda tem que aplicar o filtro de media
  String Temp;
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  //Solicita os dados do sensor
  Wire.requestFrom(MPU,14,true);  
  //Armazena o valor dos sensores nas variaveis correspondentes
  AnguloX  =	Wire.read()<<8|Wire.read();  //0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)     
  AnguloY  =	Wire.read()<<8|Wire.read();  //0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AnguloZ  =	Wire.read()<<8|Wire.read();  //0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  //Aguarda 300 ms e reinicia o processo
  delay(300);
  /* Variaveis não utilizadas
  Tmp	=	Wire.read()<<8|Wire.read();  //0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  GyX	=	Wire.read()<<8|Wire.read();  //0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  GyY	=	Wire.read()<<8|Wire.read();  //0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  GyZ	=	Wire.read()<<8|Wire.read();  //0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
  */
    
  Temp = "X ";
  Temp.concat(AnguloX);
  
  Temp = "Y ";
  Temp.concat(AnguloY);
  
  Temp = "Z ";
  Temp.concat(AnguloZ);
	
}
