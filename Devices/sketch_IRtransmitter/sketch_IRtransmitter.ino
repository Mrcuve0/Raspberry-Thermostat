#include <IRremote.h>

IRsend irsend;

void setup()
{
  Serial.begin(115200);
  Serial.println("setup done");
}

void loop() {
  irsend.sendSony(0xa90, 12);
  Serial.println("command sent");
  delay(5000); //5 second delay between each signal burst
}



 
