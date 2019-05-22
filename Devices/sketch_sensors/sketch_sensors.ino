#include "BluetoothSerial.h"
#include <WiFi.h>
#include <PubSubClient.h>
/////////////////////////////////////////////////////////////////////
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
/////////////////////////////////////////////////////////////////////
char  test_transmission[7];
char termo[7] = ":termo";
char test_ssid[6];
char ssid_id[6] = ":ssid";
char test_psw[5];
char psw_id[5] = ":psw";
/////////////////////////////////////////////////////////////////////
char ssidc[20] = "";
int ssidc_index = 0;
char ssidcreal[20] = "";
char pswc[20] = "";
int pswc_index = 0;
char pswcreal[20] = "";
int setup_done = 0;
/////////////////////////////////////////////////////////////////////
const int interruptPin = 25;
/////////////////////////////////////////////////////////////////////
char* ssid = ssidcreal;
char* psw =  pswcreal;
char* mqttServer = "";
int mqttPort;
char* mqttUser = "";
char* mqttPassword = "";
/////////////////////////////////////////////////////////////////////
char ESPname[] = "ESP32test";
/////////////////////////////////////////////////////////////////////
WiFiClient espClient;
PubSubClient client(espClient);
/////////////////////////////////////////////////////////////////////
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

/*
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP32Client", mqttUser, mqttPassword )) {
 
      Serial.println("connected");
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
  }

*/
 

void loop() {

  while(!setup_done){
    while(digitalRead(interruptPin) == HIGH){}
    Serial.println("pin low, waitiing for a transmission");
    delay(1000); 
    
    while(!SerialBT.available()){}
    test_transmission[0] = SerialBT.read();
    Serial.println(test_transmission[0]);
    test_transmission[1] = SerialBT.read();
    Serial.println(test_transmission[1]);
    test_transmission[2] = SerialBT.read();
    Serial.println(test_transmission[2]);
    test_transmission[3] = SerialBT.read();
    Serial.println(test_transmission[3]);
    test_transmission[4] = SerialBT.read();
    Serial.println(test_transmission[4]);
    test_transmission[5] = SerialBT.read();
    Serial.println(test_transmission[5]);
    
    if(strcmp(test_transmission, termo) == 0){
     Serial.println("test message recived correctly");
    } else{
     Serial.println("wrong host");  
     SerialBT.end();
    }

    for(int i = 0 ; i < 9 ; i++){
      SerialBT.write(ESPname[i]);
    }
    Serial.println("sent the ESP name");
    
    SerialBT.flush();
    
    while(!SerialBT.available()){}
    test_ssid[0] = SerialBT.read();
    Serial.println(test_ssid[0]);
    test_ssid[1] = SerialBT.read();
    Serial.println(test_ssid[1]);
    test_ssid[2] = SerialBT.read();
    Serial.println(test_ssid[2]);
    test_ssid[3] = SerialBT.read();
    Serial.println(test_ssid[3]);
    test_ssid[4] = SerialBT.read();
    Serial.println(test_ssid[4]);

    if(strcmp(test_ssid, ssid_id) == 0){
     Serial.println("ssid message recived correctly");
     Serial.println(test_ssid);
     while(SerialBT.available()){
      ssidc[ssidc_index] = SerialBT.read();
      ssidc_index++;
     }
     Serial.println(ssidc);
     Serial.println("The ssid index is");
     Serial.println(ssidc_index);
    } else{
     Serial.println("wrong ssid start"); 
     SerialBT.end(); 
    }

    for (int i = 0; i < ssidc_index-2 ; i++){
      ssidcreal[i] = ssidc[i];
    }
    Serial.print("the real ssid is ");
    Serial.println(ssidcreal);

    SerialBT.flush();

    while(!SerialBT.available()){}
    test_psw[0] = SerialBT.read();
    Serial.println(test_psw[0]);
    test_psw[1] = SerialBT.read();
    Serial.println(test_psw[1]);
    test_psw[2] = SerialBT.read();
    Serial.println(test_psw[2]);
    test_psw[3] = SerialBT.read();
    Serial.println(test_psw[3]);

    if(strcmp(test_psw, psw_id) == 0){
     Serial.println("psw message recived correctly");
     Serial.println(test_psw);
     while(SerialBT.available()){
      pswc[pswc_index] = SerialBT.read();
      pswc_index++;
     }
     Serial.println(pswc);
     Serial.println(pswc_index);
    } else{
     Serial.println("wrong psw start"); 
     SerialBT.end(); 
    }

    for (int j = 0; j < pswc_index-2 ; j++){
      pswcreal[j] = pswc[j];
    }
    Serial.print("the real psw is ");
    Serial.println(pswcreal);

    WiFi.begin(ssid, psw);
 
    while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
    
    setup_done = 1;
  }

  delay(20);

}
