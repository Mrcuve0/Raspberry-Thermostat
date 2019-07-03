#include "BluetoothSerial.h"
#include <WiFi.h>
#include <PubSubClient.h>
#include <ESPmDNS.h>
#include <WiFiClient.h>
/////////////////////////////////////////////////////////////////////
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
/////////////////////////////////////////////////////////////////////
#define interruptPin 25     //Digital pin connected to the push button
#define rele_one 23 
#define rele_two 22
#define rele_three 21
#define rele_four 19
#define rele_five 18
#define rele_six 17
#define rele_seven 16
#define rele_eight 15
/////////////////////////////////////////////////////////////////////
const char* DEVICE_ID = "DEV00";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";
IPAddress mqttServer;
/////////////////////////////////////////////////////////////////////
char termo[] = ":termo";
char test_transmission[20];
/////////////////////////////////////////////////////////////////////
char ssidc[20] = "";
char pswc[20] = "";
char mqttHostnamec[20] = "";
char roomNamec[20] = "";
/////////////////////////////////////////////////////////////////////
char* ssid = ssidc;
char* psw =  pswc;
char* mqttHostname = mqttHostnamec;
/////////////////////////////////////////////////////////////////////
int pswc_index = 0;
int ssidc_index = 0;
int mqttHostnamec_index = 0;
int test_index = 0;
int wifi_timeout = 0;
/////////////////////////////////////////////////////////////////////
char ESPname[] = "ESP32test";
char ack_char = '@';
char no_ack_char = '#';
/////////////////////////////////////////////////////////////////////
/* Stupid mechanism to wait time without stopping the cpu */
int start_time;
const int time_interval = 5000;
/////////////////////////////////////////////////////////////////////
WiFiClient espClient;
PubSubClient client(espClient);
BluetoothSerial SerialBT;
/////////////////////////////////////////////////////////////////////
void callback(char* topic, byte* payload, unsigned int length) { 
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    messageTemp += (char)payload[i];
  }
  Serial.println();

   if (String(topic) == "actuator/config") {}
    
   if (String(topic) == "esp32/output") {}
  
}
/////////////////////////////////////////////////////////////////////
void setup() {
  Serial.begin(115200);
  pinMode(interruptPin, INPUT_PULLUP);
  SerialBT.begin(ESPname); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
  client.setCallback(callback);
////////////////////////////WAITING FOR LOW PIN//////////////////////
  while(digitalRead(interruptPin) == HIGH){
    if(SerialBT.available()){
    Serial.println("wrong timing"); 
    delay(1000);
    SerialBT.end();
    ESP.restart();
    }  
  }
  Serial.println("pin low, waiting for a transmission");
////////////////////////////TEST TRANSMISSION////////////////////////
  while(!SerialBT.available()){}
  while(SerialBT.available()){
    test_transmission[test_index] = SerialBT.read();
    Serial.println(test_transmission[test_index]);
    test_index++;
    delay(40);
  }
  Serial.println(test_index);
  test_transmission[strlen(test_transmission)] = '\0';
  Serial.println(test_transmission);

  if(strcmp(test_transmission, termo) == 0){
    Serial.println("test message recived correctly");
    SerialBT.write(ack_char);
    Serial.println("sent the ack character");
  } else{
    Serial.println("wrong host"); 
    SerialBT.write(no_ack_char); 
    Serial.println("sent the no ack char");
    delay(1000);
    SerialBT.end();
    ESP.restart();
  }
//////////////////////////////WIFI///////////////////////////////////
  while(!SerialBT.available()){}
  while(SerialBT.available()){
    ssidc[ssidc_index] = SerialBT.read();
    Serial.println(ssidc[ssidc_index]);
    ssidc_index++;
    delay(40);
  }
  Serial.println(ssidc_index);
  ssidc[strlen(ssidc)] = '\0';
  Serial.println(ssid);
  SerialBT.write(ack_char);

  while(!SerialBT.available()){}
  while(SerialBT.available()){
    pswc[pswc_index] = SerialBT.read();
    Serial.println(pswc[pswc_index]);
    pswc_index++;
    delay(40);
  }
  Serial.println(pswc_index);
  pswc[strlen(pswc)] = '\0';
  Serial.println(pswc);

  WiFi.begin(ssid, psw);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    wifi_timeout++;
    if(wifi_timeout > 60){
     Serial.println("wrong credentials");  
     SerialBT.write(no_ack_char); 
     Serial.println("sent the no ack char");
     delay(1000); 
     SerialBT.end();
     ESP.restart();
    }
    Serial.println("Connecting to WiFi..");
  }

  Serial.println("Connected to the WiFi network");
  SerialBT.write(ack_char);
  Serial.println("sent the ack char"); 
//////////////////////////////MQTT///////////////////////////////////
  while(!SerialBT.available()){}
  while(SerialBT.available()){
    mqttHostnamec[mqttHostnamec_index] = SerialBT.read();
    Serial.println(mqttHostnamec[mqttHostnamec_index]);
    mqttHostnamec_index++;
    delay(40);
  }
  Serial.println(mqttHostnamec_index);
  mqttHostnamec[strlen(mqttHostnamec)] = '\0';
  Serial.println(mqttHostnamec);


  if (!MDNS.begin(DEVICE_ID)) {
    Serial.println("Error setting up MDNS responder!");
    delay(1000);
    SerialBT.write(no_ack_char); 
    Serial.println("sent the no ack char");
    delay(1000); 
    SerialBT.end();
    ESP.restart();
  }
  
   
  Serial.println("mDNS responder started");
  // Look for the local IP of the rasbperry pi 
  mqttServer = MDNS.queryHost(mqttHostname);
  Serial.print("IP address of server: ");
  Serial.println(mqttServer.toString());
  // Connect to the MQTT broker 
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
    
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
      
    //if (client.connect("ESP32Client", mqttUser, mqttPassword )) {
    if (client.connect(ESPname, mqttUser, mqttPassword )) {
      Serial.println("Connected to the broker");
      SerialBT.write(ack_char);
      Serial.println("sent the ack char");
    } else {
      Serial.println("wrong credentials for the broker");  
      SerialBT.write(no_ack_char); 
      Serial.println("sent the no ack char");
      delay(1000); 
      SerialBT.end();
      ESP.restart();
    }
    
  }
  
  Serial.println("setup done, everything is connected");
  SerialBT.end();
  Serial.println("SerialBT ended");
  
  start_time = millis();
  Serial.println("initialized the start time");

  
}

/////////////////////////////////////////////////////////////////////
void loop() {
  
 
}
