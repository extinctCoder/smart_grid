DC 0-25V Mini Voltage Sensor Module for Arduino .

### Features 
- Voltage input range: DC 0-25V  
- Voltage detection range: DC 0.02445V-25V  
- Voltage Analog Resolution: 0.00489V  
- DC input connector: Terminal cathode connected to VCC, GND negative pole  
- Output interface: "+" connect 5/3.3V, "-" connect GND, "s" connect the Arduino AD pins   
### Reference code:  
``` cpp
#include <Wire.h>  
int val11;   
int val2;

void setup()   
{     
 pinMode(LED1,OUTPUT);     
 Serial.begin(9600);     
 Serial.println("Emartee.Com");     
 Serial.println("Voltage: ");     
 Serial.print("V");   
}   
void loop()   
{         
 float temp;         
 val11=analogRead(1);         
 temp=val11/4.092;         
 val11=(int)temp;//         
 val2=((val11%100)/10);         
 Serial.println(val2);            
 delay(1000);   
}
```