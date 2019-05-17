#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiClient.h>
#include "PubSubClient.h"

/* Unique ID of the sensor/actuator */
const char* DEVICE_ID = "DEV00";
/* Wifi connection credentials */
char* ssid = "Poldo";
char* password =  "poldododo";
/* MQTT broker connection credentials */
IPAddress mqttServer;
char* mqttHostname = "thermostat";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";
/* Stupid mechanism to wait time without stopping the cpu */
int start_time;
const int time_interval = 5000;

WiFiClient espClient;
PubSubClient client(espClient);

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
 
void setup() {
  /* Init serial communication for debug purposes */
  Serial.begin(115200);
  /* Loop to establish Wifi connection */ 
  WiFi.begin(ssid, password);
  int timeout = 10;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
    timeout--;
    if (!timeout){
      WiFi.begin(ssid, password);
      timeout = 10;
    }
  }
  Serial.println("Connected to the WiFi network");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  /* Init multicast-DNS */
  if (!MDNS.begin(DEVICE_ID)) {
      Serial.println("Error setting up MDNS responder!");
      while(1) {
          delay(1000);
      }
  }
  Serial.println("mDNS responder started");
  /* Look for the local IP of the rasbperry pi */
  mqttServer = MDNS.queryHost(mqttHostname);
  Serial.print("IP address of server: ");
  Serial.println(mqttServer.toString());
  /* Connect to the MQTT broker */ 
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
  client.publish("sensors", "mock data");
  client.subscribe("actuators");
  start_time = millis();
}
 
void loop() {
  client.loop();
  if (millis() - start_time > time_interval){
    client.publish("sensors", "mock data");
    start_time = millis();
  }
}
