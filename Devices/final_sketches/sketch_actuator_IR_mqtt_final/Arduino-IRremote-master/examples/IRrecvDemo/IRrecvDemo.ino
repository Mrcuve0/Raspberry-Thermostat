/*
 * IRremote: IRrecvDemo - demonstrates receiving IR codes with IRrecv
 * An IR detector/demodulator must be connected to the input RECV_PIN.
 * Version 0.1 July, 2009
 * Copyright 2009 Ken Shirriff
 * http://arcfn.com
 */

#include <IRremote.h>
 
int RECV_PIN = 15;
 
IRrecv irrecv(RECV_PIN);
 
decode_results results;
 
void setup()
{
  Serial.begin(115200);
  Serial.println("IR enabled");
  irrecv.enableIRIn(); // Start the receiver
}
 
void loop()
{
  if (irrecv.decode(&results))
  {
    Serial.print("the start is ");
    Serial.println(results.decode_type);
    Serial.println(results.value);
    Serial.println(results.value, HEX);
    irrecv.resume();
  }
}
