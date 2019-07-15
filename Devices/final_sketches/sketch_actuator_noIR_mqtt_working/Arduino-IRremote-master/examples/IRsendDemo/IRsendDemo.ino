/*
 * IRremote: IRsendDemo - demonstrates sending IR codes with IRsend
 * An IR LED must be connected to Arduino PWM pin 3.
 * Version 0.1 July, 2009
 * Copyright 2009 Ken Shirriff
 * http://arcfn.com
 */


#include <IRremote.h>

IRsend irsend;
unsigned long code = 50;

void setup()
{
  Serial.begin(115200);
}

void loop() {
  irsend.sendRC5(code, 12);
  Serial.println("command sent RC5");
	delay(1000); //5 second delay between each signal burst
  
  irsend.sendRC6(code, 12);
  Serial.println("command sent RC6");
  delay(1000); //5 second delay between each signal burst
  /*
  irsend.sendNEC(code, 12);
  Serial.println("command sent NEC");
  delay(1000); //5 second delay between each signal burst
  
  irsend.sendSAMSUNG(code, 12);
  Serial.println("command sent samsung");
  delay(1000); //5 second delay between each signal burst
  
  irsend.sendLG(code, 12);
  Serial.println("command sent LG");
  delay(1000); //5 second delay between each signal burst
  
  irsend.sendPanasonic(code, 12);
  Serial.println("command sent panasonic");
  delay(1000); //5 second delay between each signal burst
  */
  
}
