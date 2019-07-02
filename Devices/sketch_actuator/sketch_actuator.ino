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
const int interruptPin = 25;
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
/////////////////////////////////////////////////////////////////////
char* ssid = ssidc;
char* psw =  pswc;
char* mqttHostname = mqttHostnamec;
/////////////////////////////////////////////////////////////////////
int setup_done = 0;
/////////////////////////////////////////////////////////////////////
int pswc_index = 0;
int ssidc_index = 0;
int mqttHostnamec_index = 0;
int test_index = 0;
int wifi_timeout = 0;
int broker_timeout = 0;
int roomNamec_index = 0;
/////////////////////////////////////////////////////////////////////
char ESPname[] = "ESP32test";
char ack_char = '@';
char no_ack_char = '#';
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
    while(digitalRead(interruptPin) == HIGH){
      if(SerialBT.available()){
        //Serial.println("wrong timing"); 
        SerialBT.write(no_ack_char); 
        //Serial.println("sent the no ack char");
        delay(1000);
        SerialBT.end();
        BluetoothSerial SerialBT;
        SerialBT.begin(ESPname);
        //Serial.println("The device started, now you can pair it with bluetooth!");
        break;
      }  
    }
    //Serial.println("pin low, waiting for a transmission");
    delay(1000);

    while(!SerialBT.available()){}
//////////////////////synchronization///////////////////////////////
    while(SerialBT.available()){
      test_transmission[test_index] = SerialBT.read();
      //Serial.println(test_transmission[test_index]);
      test_index++;
      delay(40);
    }
    //Serial.println(test_index);
    test_transmission[strlen(test_transmission)] = '\0';
    //Serial.println(test_transmission);

    if(strcmp(test_transmission, termo) == 0){
     //Serial.println("test message recived correctly");
     SerialBT.write(ack_char);
     //Serial.println("sent the ack character");
    } else{
     //Serial.println("wrong host"); 
     SerialBT.write(no_ack_char); 
     //Serial.println("sent the no ack char");
     delay(1000);
     SerialBT.end();
     BluetoothSerial SerialBT;
     SerialBT.begin(ESPname);
     //Serial.println("The device started, now you can pair it with bluetooth!");
     break;
    }

//////////////////////WIFI ssid///////////////////////////////
    SerialBT.flush();
    while(!SerialBT.available()){}

    while(SerialBT.available()){
      ssidc[ssidc_index] = SerialBT.read();
      //Serial.println(ssidc[ssidc_index]);
      ssidc_index++;
      delay(40);
    }
    //Serial.println(ssidc_index);
    ssidc[strlen(ssidc)] = '\0';
    //Serial.println(ssid);
//////////////////////WIFI psw///////////////////////////////    
    SerialBT.flush();
    while(!SerialBT.available()){}

    while(SerialBT.available()){
      pswc[pswc_index] = SerialBT.read();
      //Serial.println(pswc[pswc_index]);
      pswc_index++;
      delay(40);
    }
    //Serial.println(pswc_index);
    pswc[strlen(pswc)] = '\0';
    //Serial.println(pswc);

    SerialBT.flush();
//////////////////////WIFI connection///////////////////////////
    WiFi.begin(ssid, psw);
 
    while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    wifi_timeout++;
    if(wifi_timeout > 30){
     //Serial.println("wrong credentials");  
     SerialBT.write(no_ack_char); 
     //Serial.println("sent the no ack char");
     delay(1000); 
     SerialBT.end();
     BluetoothSerial SerialBT;
     SerialBT.begin(ESPname);
     //Serial.println("The device started, now you can pair it with bluetooth!");
     wifi_timeout = 0;
     break;
    }
    //Serial.println("Connecting to WiFi..");
    }
 
    //Serial.println("Connected to the WiFi network");
    SerialBT.write(ack_char);
    //Serial.println("sent the ack char");
    
//////////////////////mqtt Server///////////////////////////////
    SerialBT.flush();
    while(!SerialBT.available()){}

    while(SerialBT.available()){
      mqttHostnamec[mqttHostnamec_index] = SerialBT.read();
      //Serial.println(mqttHostnamec[mqttHostnamec_index]);
      mqttHostnamec_index++;
      delay(40);
    }
    //Serial.println(mqttHostnamec_index);
    mqttHostnamec[strlen(mqttHostnamec)] = '\0';
    //Serial.println(mqttHostnamec);

    if (!MDNS.begin(DEVICE_ID)) {
      //Serial.println("Error setting up MDNS responder!");
      while(1) {
        delay(1000);
      }
    }
    
    //Serial.println("mDNS responder started");
    /* Look for the local IP of the rasbperry pi */
    mqttServer = MDNS.queryHost(mqttHostname);
    //Serial.print("IP address of server: ");
    //Serial.println(mqttServer.toString());
    /* Connect to the MQTT broker */ 
    client.setServer(mqttServer, mqttPort);
    client.setCallback(callback);
    
    while (!client.connected()) {
      //Serial.println("Connecting to MQTT...");
      broker_timeout ++;
      if(broker_timeout > 30){
        //Serial.println("wrong credentials for the broker");  
        SerialBT.write(no_ack_char); 
        //Serial.println("sent the no ack char");
        delay(1000); 
        SerialBT.end();
        BluetoothSerial SerialBT;
        SerialBT.begin(ESPname);
        //Serial.println("The device started, now you can pair it with bluetooth!");
        broker_timeout = 0;
        break;
      }
      //if (client.connect("ESP32Client", mqttUser, mqttPassword )) {
      if (client.connect(ESPname, mqttUser, mqttPassword )) {
        //Serial.println("Connected to the broker");
        SerialBT.write(ack_char);
        //Serial.println("sent the ack char");
      } else {
        //Serial.println("wrong credentials for the broker");  
        SerialBT.write(no_ack_char); 
        //Serial.println("sent the no ack char");
        delay(1000); 
        SerialBT.end();
        BluetoothSerial SerialBT;
        SerialBT.begin(ESPname);
        //Serial.println("The device started, now you can pair it with bluetooth!");
        broker_timeout = 0;
        break;
      }
      delay(500);
    }
    
    setup_done = 1;
    //Serial.println("setup done");
   }
  //code here
}
