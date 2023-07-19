#include <LiquidCrystal.h>
#include <DallasTemperature.h>
#include <OneWire.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2); //0x27

int phval = 0;
unsigned long int avgval;
int buffer_arr[10],temp;
OneWire ourWire(2);
DallasTemperature sensors(&ourWire);


void setup()
{
  Wire.begin();
  Serial.begin(9600);
//  Serial.println("start");
  sensors.begin();
  lcd.init();
//  Serial.println("CLEARDATA");
//  Serial.println("LABEL,pH,temp,EC");
}

void loop() {
  char ReceivedByte  = "0";
sensors.requestTemperatures();
int value = analogRead(A1);
float ec_value = value * 34;
for(int i=0;i<10;i++)
{
buffer_arr[i]=analogRead(A0);
delay(30);
}
for(int i=0;i<9;i++)
{
for(int j=i+1;j<10;j++)
{
if(buffer_arr[i]>buffer_arr[j])
{
temp=buffer_arr[i];
buffer_arr[i]=buffer_arr[j];
buffer_arr[j]=temp;
}
}
}
avgval=0;
for(int i=2;i<8;i++)
avgval+=buffer_arr[i];
int sensorValue = analogRead(A0);
float volt = sensorValue*5.0/1024;
//float ph_act = -9.457 * volt + 37.62;
float ph_act = 7 + ((3.52 - volt) * 8.22);

//========================================
//Serial.print("DATA,");
//Serial.print("pH: ");
if (Serial.available() > 0) //Wait for data reception
{
     ReceivedByte = Serial.read();//Read data from Arduino Serial UART buffer

     if (ReceivedByte == '$')//Check received byte is $
     {
      Serial.print(ph_act);
      Serial.print("-");
      //Serial.print("Temp= ");
      Serial.print(sensors.getTempCByIndex(0));
      Serial.print("-");
      //Serial.print("EC= ");
      Serial.print(ec_value);
      Serial.print("-");
      Serial.println();
      delay(1000);
     }
 }
//Serial.print(ph_act);
//      Serial.print("-");
//      //Serial.print("Temp= ");
//      Serial.print(sensors.getTempCByIndex(0));
//      Serial.print("-");
//      //Serial.print("EC= ");
//      Serial.print(ec_value);
//      Serial.print("-");
//      Serial.println();
//      delay(1000);

lcd.setCursor(1,0);
lcd.print("T=");
lcd.setCursor(3,0);
lcd.print(sensors.getTempCByIndex(0));
lcd.setCursor(1,1);
lcd.print("pH=");
lcd.setCursor(4,1);
lcd.print(ph_act);
delay(10);
}
