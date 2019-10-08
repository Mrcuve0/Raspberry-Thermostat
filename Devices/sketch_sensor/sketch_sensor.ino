// Copyright (C) 2019 Paolo Calao, Samuele Yves Cerini, Federico Pozzana


// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

#include "BluetoothSerial.h"
#include <WiFi.h>
#include "PubSubClient.h"
#include <ESPmDNS.h>
#include <WiFiClient.h>
#include "Adafruit_Sensor.h"
#include "DHT.h"
#include "IRremote.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

#define interruptPin 25 //Digital pin connected to the push button
#define DHTPIN 27       // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22

//stuff for IR functionalities///////////
int RECV_PIN = 15;
unsigned long code = 50;  //default code
IRrecv irrecv(RECV_PIN);
IRsend irsend;
decode_results results;
/////////////////////////////////////////

const char *DEVICE_ID = "DEV00";
const int mqttPort = 1883;
const char *mqttUser = "";
const char *mqttPassword = "";
IPAddress mqttServer;

char termo[] = ":termo";
char test_transmission[20];

// float *temperature;
float temperature;
char temp[6];
String temp_str;

char ssidc[64] = "";
char pswc[64] = "";
char mqttHostnamec[20] = "";
char roomNamec[20] = "";

char *ssid = ssidc;
char *psw = pswc;
char *mqttHostname = mqttHostnamec;
char *roomName = roomNamec;

int pswc_index = 0;
int ssidc_index = 0;
int mqttHostnamec_index = 0;
int test_index = 0;
int wifi_timeout = 0;
int roomNamec_index = 0;

// Device ID, change this for each ESP you are going to flash
char ESPname[] = "Sensor 1";
char ack_char = '@';
char no_ack_char = '#';

WiFiClient espClient;
PubSubClient client(espClient);
BluetoothSerial SerialBT;
DHT dht(DHTPIN, DHTTYPE);

/* Stupid mechanism to wait time without stopping the cpu */
int start_time;
const int time_interval = 5000;

void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++)
  {
    Serial.print((char)payload[i]);
    messageTemp += (char)payload[i];
  }
  Serial.println();

  if (String(topic) == "airconditioning/ESPname"){      //ESPname is the ID
    if (messageTemp == "ON"){
      irsend.sendRC5(code, 12);
      Serial.println("command sent");
    }else if (messageTemp == "OFF"){
      irsend.sendRC5(code, 12);
      Serial.println("command sent");
    }
  }
}

void setup()
{
  Serial.begin(115200);
  dht.begin();
  pinMode(interruptPin, INPUT_PULLUP);
///////////////////////////////////////////////////////////////////////
  Serial.println("IR enabled");
  irrecv.enableIRIn(); // Start the receiver
///////////////////////////////////////////////////////////////////////
  SerialBT.begin(ESPname); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");

  ////////////////////////////WAITING FOR LOW PIN//////////////////////
  while (digitalRead(interruptPin) == HIGH)
  {
    if (SerialBT.available())
    {
      Serial.println("wrong timing");
      delay(1000);
      SerialBT.end();
      ESP.restart();
    }
  }
  Serial.println("pin low, waiting for a transmission");

  ////////////////////////////TEST TRANSMISSION////////////////////////
  while (!SerialBT.available())
  {
  }
  while (SerialBT.available())
  {
    test_transmission[test_index] = SerialBT.read();
    Serial.println(test_transmission[test_index]);
    test_index++;
    delay(40);
  }
  Serial.println(test_index);
  test_transmission[strlen(test_transmission)] = '\0';
  Serial.println(test_transmission);

  if (strcmp(test_transmission, termo) == 0)
  {
    Serial.println("test message recived correctly");
    SerialBT.write(ack_char);
    Serial.println("sent the ack character");
  }
  else
  {
    Serial.println("wrong host");
    SerialBT.write(no_ack_char);
    Serial.println("sent the no ack char");
    delay(1000);
    SerialBT.end();
    ESP.restart();
  }

  //////////////////////////////WIFI///////////////////////////////////
  while (!SerialBT.available())
  {
  }
  while (SerialBT.available())
  {
    ssidc[ssidc_index] = SerialBT.read();
    Serial.println(ssidc[ssidc_index]);
    ssidc_index++;
    delay(40);
  }
  Serial.println(ssidc_index);
  ssidc[strlen(ssidc)] = '\0';
  Serial.println(ssid);
  SerialBT.write(ack_char);

  while (!SerialBT.available())
  {
  }
  while (SerialBT.available())
  {
    pswc[pswc_index] = SerialBT.read();
    Serial.println(pswc[pswc_index]);
    pswc_index++;
    delay(40);
  }
  Serial.println(pswc_index);
  pswc[strlen(pswc)] = '\0';
  Serial.println(pswc);

  WiFi.begin(ssid, psw);
  delay(500);
  wifi_timeout = 0;
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to WiFi..");
    wifi_timeout++;
    if (wifi_timeout % 10 == 0)
    {
      Serial.println("\t--> Retry...");
      WiFi.begin(ssid, psw);
    }
    if (wifi_timeout > 60)
    {
      Serial.println("wrong credentials");
      SerialBT.write(no_ack_char);
      Serial.println("sent the no ack char");
      delay(1000);
      SerialBT.end();
      ESP.restart();
    }
  }

  // WiFi.begin(ssid, psw);
  // int timeout = 10;
  // while (WiFi.status() != WL_CONNECTED)
  // {
  //   delay(500);
  //   Serial.println("Connecting to WiFi..");
  //   timeout--;
  //   if (!timeout)
  //   {
  //     WiFi.begin(ssid, psw);
  //     timeout = 10;
  //   }
  // }

  Serial.println("Connected to the WiFi network");
  SerialBT.write(ack_char);
  Serial.println("sent the ack char");

  //////////////////////////////MQTT///////////////////////////////////
  while (!SerialBT.available())
  {
  }
  while (SerialBT.available())
  {
    mqttHostnamec[mqttHostnamec_index] = SerialBT.read();
    Serial.println(mqttHostnamec[mqttHostnamec_index]);
    mqttHostnamec_index++;
    delay(40);
  }
  Serial.println(mqttHostnamec_index);
  mqttHostnamec[strlen(mqttHostnamec)] = '\0';
  Serial.println(mqttHostnamec);

  if (!MDNS.begin(DEVICE_ID))
  {
    Serial.println("Error setting up MDNS responder!");
    delay(1000);
    SerialBT.write(no_ack_char);
    Serial.println("sent the no ack char");
    delay(1000);
    SerialBT.end();
    ESP.restart();
  }

  int mDNS_timeout = 0;
  Serial.println("mDNS responder started");
  mqttServer = MDNS.queryHost(mqttHostname);
  while (mqttServer.toString() == "0.0.0.0")
  {
    mDNS_timeout++;
    Serial.println("Trying again to resolve mDNS");
    delay(250);
    mqttServer = MDNS.queryHost(mqttHostname);
    if (mDNS_timeout > 20)
    {
      Serial.println("Error setting up MDNS responder!");
      delay(1000);
      SerialBT.write(no_ack_char);
      Serial.println("sent the no ack char");
      delay(1000);
      SerialBT.end();
      ESP.restart();
    }
  }
  Serial.print("IP address of server: ");
  Serial.println(mqttServer.toString());
  Serial.println("Done finding the mDNS details...");

  // Connect to the MQTT broker
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected())
  {
    Serial.println("Connecting to MQTT...");

    //if (client.connect("ESP32Client", mqttUser, mqttPassword )) {
    if (client.connect(ESPname, mqttUser, mqttPassword))
    {
      Serial.println("Connected to the broker");
      SerialBT.write(ack_char);
      Serial.println("sent the ack char");
    }
    else
    {
      Serial.println("wrong credentials for the broker");
      SerialBT.write(no_ack_char);
      Serial.println("sent the no ack char");
      delay(1000);
      SerialBT.end();
      ESP.restart();
    }
  }

  //////////////////////////////ROOM///////////////////////////////////
  while (!SerialBT.available())
  {
  }
  while (SerialBT.available())
  {
    roomNamec[roomNamec_index] = SerialBT.read();
    Serial.println(roomNamec[roomNamec_index]);
    roomNamec_index++;
    delay(40);
  }
  Serial.println(roomNamec_index);
  roomNamec[strlen(roomNamec)] = '\0';
  Serial.println(roomNamec);
  SerialBT.write(ack_char);

  Serial.println("setup done, everything is connected");
  // SerialBT.end();
  Serial.println("SerialBT NOT ended");

  client.subscribe("airconditioning/ESPname");                    //ESPname has to be changed with a number (the ID)
  Serial.println("Subscribed to airconditioning topic");

///////////////new IR code//////////////////////////////////////////
  Serial.println("looking for a new IR code");
  while (digitalRead(interruptPin) == HIGH){
    if (irrecv.decode(&results)){
      code = results.value;
      Serial.print("new code is ");
      Serial.println(code);
    }
  }
  Serial.println("IR setup done");
////////////////////////////////////////////////////////////////////

  start_time = millis();
  Serial.println("initialized the start time");
}

void loop()
{
  if (millis() - start_time > time_interval)
  {
    temperature = dht.readTemperature();

    temp_str = String(temperature);
    temp_str.toCharArray(temp, temp_str.length() + 1);

    Serial.print("temperature: ");
    Serial.println(temperature);
    client.publish("temperature/ESPname", temp); //ESPname has to be changed with a number (the ID)
    start_time = millis();
  }
}
