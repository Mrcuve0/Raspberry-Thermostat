#include "BluetoothSerial.h"
#include <WiFi.h>
#include <PubSubClient.h>
/////////////////////////////////////////////////////////////////////
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
/////////////////////////////////////////////////////////////////////
const int interruptPin = 25;
/////////////////////////////////////////////////////////////////////
char termo[] = ":termo";
char test_transmission[20];
/////////////////////////////////////////////////////////////////////
char ssidc[20] = "";
char pswc[20] = "";
char mqttServerc[20] = "";
/////////////////////////////////////////////////////////////////////
char* ssid = ssidc;
char* psw =  pswc;
char* mqttServer = mqttServerc;
/////////////////////////////////////////////////////////////////////
int setup_done = 0;
/////////////////////////////////////////////////////////////////////
int pswc_index = 0;
int ssidc_index = 0;
int mqttServerc_index = 0;
int test_index = 0;
int wifi_timeout = 0;
/////////////////////////////////////////////////////////////////////
char ESPname[] = "ESP32test";
/////////////////////////////////////////////////////////////////////
WiFiClient espClient;
PubSubClient client(espClient);
BluetoothSerial SerialBT;
/////////////////////////////////////////////////////////////////////
void callback(char* topic, byte* payload, unsigned int length) { 
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
 
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
 
  Serial.println();
  Serial.println("-----------------------");
}
/////////////////////////////////////////////////////////////////////
void setup() {
  Serial.begin(115200);
  pinMode(interruptPin, INPUT_PULLUP);
  SerialBT.begin(ESPname); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
}
/////////////////////////////////////////////////////////////////////
void loop() {
  while(!setup_done){
    while(digitalRead(interruptPin) == HIGH){}
    Serial.println("pin low, waiting for a transmission");
    delay(1000);

    while(!SerialBT.available()){}
//////////////////////synchronization///////////////////////////////
    while(SerialBT.available()){
      test_transmission[test_index] = SerialBT.read();
      Serial.println(test_transmission[test_index]);
      test_index++;
    }
    Serial.println(test_index);
    test_transmission[strlen(test_transmission)] = '\0';
    Serial.println(test_transmission);

    if(strcmp(test_transmission, termo) == 0){
     Serial.println("test message recived correctly");
    } else{
     Serial.println("wrong host");  
     SerialBT.end();
     BluetoothSerial SerialBT;
     SerialBT.begin(ESPname);
     Serial.println("The device started, now you can pair it with bluetooth!");
     break;
    }

    for(int i = 0 ; i < 9 ; i++){
      SerialBT.write(ESPname[i]);
    }
    Serial.println("sent the ESP name");
//////////////////////WIFI ssid///////////////////////////////
    SerialBT.flush();
    while(!SerialBT.available()){}

    while(SerialBT.available()){
      ssidc[ssidc_index] = SerialBT.read();
      Serial.println(ssidc[ssidc_index]);
      ssidc_index++;
    }
    Serial.println(ssidc_index);
    ssidc[strlen(ssidc)] = '\0';
    Serial.println(ssid);
//////////////////////WIFI psw///////////////////////////////    
    SerialBT.flush();
    while(!SerialBT.available()){}

    while(SerialBT.available()){
      pswc[pswc_index] = SerialBT.read();
      Serial.println(pswc[pswc_index]);
      pswc_index++;
    }
    Serial.println(pswc_index);
    pswc[strlen(pswc)] = '\0';
    Serial.println(pswc);

    SerialBT.flush();
//////////////////////WIFI connection///////////////////////////
    WiFi.begin(ssid, psw);
 
    while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    wifi_timeout++;
    if(wifi_timeout > 30){
     Serial.println("wrong credentials");  
     SerialBT.end();
     BluetoothSerial SerialBT;
     SerialBT.begin(ESPname);
     Serial.println("The device started, now you can pair it with bluetooth!");
     wifi_timeout = 0;
     break;
    }
    Serial.println("Connecting to WiFi..");
    }
 
    Serial.println("Connected to the WiFi network");
//////////////////////mqtt Server///////////////////////////////
    SerialBT.flush();
    while(!SerialBT.available()){}

    while(SerialBT.available()){
      mqttServerc[mqttServerc_index] = SerialBT.read();
      Serial.println(mqttServerc[mqttServerc_index]);
      mqttServerc_index++;
    }
    Serial.println(mqttServerc_index);
    mqttServerc[strlen(mqttServerc)] = '\0';
    Serial.println(mqttServerc);
    
    setup_done = 1;
   }
    
}
