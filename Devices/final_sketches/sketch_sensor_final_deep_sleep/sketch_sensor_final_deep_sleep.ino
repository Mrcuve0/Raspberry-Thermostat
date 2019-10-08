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

#include "EEPROM.h"
#include "BluetoothSerial.h"
#include <WiFi.h>
#include <WiFiClient.h>
#include <alloca.h>
#include <string>
#include <cstring>
#include <string.h>
#include "PubSubClient.h"
#include <ESPmDNS.h>
#include "Adafruit_Sensor.h"
#include "DHT.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

#define EEPROM_SIZE 256

#define interruptPin 25 //Digital pin connected to the push button
#define DHTPIN 27       // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22
#define resetPin 26
#define greenLed 33 //used for BT transmission
#define blueLed 35  //used for reconnection

#define TIME_TO_SLEEP 30       /* Time ESP32 will go to sleep (in seconds) */
#define uS_TO_S_FACTOR 1000000 /* Conversion factor for micro seconds to seconds */

//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////
/*first address is test
 * second address is ssid max capacity
 * third address is psw max capacity
 * fourth address is hostname max capacity
 * fifth address is roomname max capacity
 * sixth address is room ID
 */
int address = 0;
int addressone = 1;
int addresstwo = 65;
int addressthree = 129;
int addressfour = 149;
int addressfive = 169;
//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

const char *DEVICE_ID = "DEV01";
const int mqttPort = 1883;
const char *mqttUser = "";
const char *mqttPassword = "";
IPAddress mqttServer;

//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////
//char* airConditioningTopic = "airconditioning/";
//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

char termo[] = ":termo";
char test_transmission[20];

// float *temperature;
float temperature;
char temp[6];
String temp_str;

char ssidc[64] = "";
char pswc[64] = "";
char roomNamec[20] = "";
char testc;
char roomIDc;

char *ssid = ssidc;
char *psw = pswc;
char *mqttHostname = "thermostat";
char *roomName = roomNamec;

int pswc_index = 0;
int ssidc_index = 0;
int test_index = 0;
int wifi_timeout = 0;
int roomNamec_index = 0;

// Device ID, change this for each ESP you are going to flash
char ESPname[] = "1";
char ack_char = '@';
char no_ack_char = '#';

//temperatures    stanza : ID
//                room_name : stringa nome stanza
//                temp : numero

String stanza_string = "{\"room\": \"";
String temp_string = "\", \"temperature\": ";
String closing_string = "}";
String temperature_string = "";

WiFiClient espClient;
BluetoothSerial SerialBT;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);

/* Stupid mechanism to wait time without stopping the cpu */
int start_time;
const int time_interval = 15000;

void IRAM_ATTR handleInterrupt();

void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  std::string messageTemp;
  Serial.println();
  Serial.println("------------------------------------");

  for (int i = 0; i < length; i++)
  {
    Serial.print((char)payload[i]);
    messageTemp += (char)payload[i];
  }
  Serial.println();
  Serial.println("------------------------------------");
}

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(115200);
  dht.begin();
  pinMode(interruptPin, INPUT_PULLUP);
  pinMode(greenLed, OUTPUT);
  pinMode(blueLed, OUTPUT);
  pinMode(resetPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(resetPin), handleInterrupt, FALLING);
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  Serial.println("esp sleep enabled");

  Serial.println("before initializing EEPROM");

  if (!EEPROM.begin(EEPROM_SIZE))
  {
    Serial.println("Failed to initialise EEPROM");
    Serial.println("Restarting...");
    delay(1000);
    ESP.restart();
  }

  Serial.println("after initializing EEPROM");

  if (EEPROM.readChar(address) == 'F')
  { //ack char for credentials
    //credentials already stored in eeprom
    Serial.println("eeprom connection in if {}");
    showCredentials();
    digitalWrite(blueLed, HIGH);
    eepromConnection();
    digitalWrite(blueLed, LOW);
  }
  else
  {
    //credentials not yet stored in eeprom
    Serial.println("normal connection in else {}");
    digitalWrite(blueLed, HIGH);
    normalConnection();
    digitalWrite(blueLed, LOW);
  }

  if (client.subscribe("temperatures") == false)
  {
    Serial.println("not subscribed to temperatures topic");
  }
  Serial.println("subscribed to temperatures topic");

  if (!client.connected())
  {
    Serial.println("client not connected");
    //ESP.restart();
    digitalWrite(blueLed, HIGH);
    reconnect();
    digitalWrite(blueLed, LOW);
    if (client.subscribe("temperatures") == false)
    {
      Serial.println("not subscribed to temperatures topic");
    }
    Serial.println("subscribed to temperatures topic");
  }

  temperature = dht.readTemperature();

  temp_str = String(temperature);
  temp_str.toCharArray(temp, temp_str.length() + 1);

  Serial.print("temperature: ");
  Serial.println(temperature);

  Serial.println("concatenating strings");
  temperature_string += stanza_string;
  temperature_string += roomIDc;
  temperature_string += temp_string;
  temperature_string += temp_str;
  temperature_string += closing_string;
  Serial.println(temperature_string);

  client.publish("temperatures", temperature_string.c_str());
  temperature_string = "";

  client.loop();
  Serial.println("Going to sleep now");
  esp_deep_sleep_start();
}

void loop()
{
}

///////////////////////////////////////////////////////////////////
void IRAM_ATTR handleInterrupt()
{
  Serial.println("reset button pressed");
  delay(1000);
  clearEEPROM();
  ESP.restart();
}

void waitingLowPin()
{
  ////////////////////////////WAITING FOR LOW PIN//////////////////////
  SerialBT.begin(ESPname); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
  digitalWrite(greenLed, HIGH);
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
  digitalWrite(greenLed, LOW);
}

void testTransmission()
{
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
}

void ssidpsw()
{
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
}

void wifiConnection()
{

  WiFi.begin(ssid, psw);
  delay(500);
  wifi_timeout = 0;
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to WiFi..");
    wifi_timeout++;
    if (wifi_timeout % 5 == 0)
    {
      Serial.println("\t--> Retry...");
      WiFi.begin(ssid, psw);
    }
  }

  Serial.println("Connected to the WiFi network");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  SerialBT.write(ack_char);
  Serial.println("sent the ack char");
}

void mqttConnection()
{
  if (!MDNS.begin(DEVICE_ID))
  {
    Serial.println("Error setting up MDNS responder!");
    delay(1000);
    ESP.restart();
    return;
  }

  Serial.println("mDNS responder started");
  // Look for the local IP of the rasbperry pi
  mqttServer = MDNS.queryHost(mqttHostname);

  while (mqttServer.toString() == "0.0.0.0")
  {
    Serial.println("Trying again to resolve mDNS");
    delay(250);
    mqttServer = MDNS.queryHost(mqttHostname);
  }

  Serial.print("IP address of server: ");
  Serial.println(mqttServer.toString());
  // Connect to the MQTT broker
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  while (!client.connected())
  {
    Serial.println("Connecting to MQTT...");
    if (client.connect(DEVICE_ID, mqttUser, mqttPassword))
    {
      Serial.println("connected to the broker");
    }
    else
    {
      /*Serial.print("failed with state ");
        Serial.print(client.state());
        delay(1000);
        Serial.println("wrong credentials, have to restart the esp32");
        clearEEPROM();
        delay(1000);
        ESP.restart();*/
    }
  }
}

void room()
{
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
  Serial.print("roomIDc is ");
  roomIDc = roomNamec[roomNamec_index - 1];
  Serial.println(roomIDc);
  SerialBT.write(ack_char);
  Serial.println("sent the ack char for roomName");
}
////////////////////////////////////////////////////////////////////////

void showCredentials()
{
  //taking the credentials from EEPROM
  testc = EEPROM.readChar(address);
  EEPROM.readString(addressone).toCharArray(ssidc, 64);
  EEPROM.readString(addresstwo).toCharArray(pswc, 64);
  //EEPROM.readString(addressthree).toCharArray(mqttHostnamec,20);
  EEPROM.readString(addressfour).toCharArray(roomNamec, 20);
  roomIDc = EEPROM.readChar(addressfive);
  //printing the credentials from EEPROM
  Serial.print("test is ");
  Serial.println(testc);
  Serial.print("ssid is ");
  Serial.println(ssidc);
  Serial.print("psw is ");
  Serial.println(pswc);
  //Serial.print("mqttHostname is ");
  //Serial.println(mqttHostnamec);
  Serial.print("roomName is ");
  Serial.println(roomNamec);
  Serial.print("room ID is ");
  Serial.println(roomIDc);
}

void clearEEPROM()
{
  for (int i = 0; i < EEPROM_SIZE; ++i)
  {
    EEPROM.writeChar(i, '\0');
  }
  EEPROM.commit();
  Serial.println("EEPROM cleared");
}

void reconnect()
{

  //////////WIFI CONNECTION/////////////////////////////////////////
  WiFi.begin(ssid, psw);
  delay(500);
  wifi_timeout = 0;
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to WiFi..");
    wifi_timeout++;
    if (wifi_timeout % 5 == 0)
    {
      Serial.println("\t--> Retry...");
      WiFi.begin(ssid, psw);
    }
  }

  Serial.println("Connected to the WiFi network");

  //////////MQTT CONNECTION/////////////////////////////////////////

  if (!MDNS.begin(DEVICE_ID))
  {
    Serial.println("Error setting up MDNS responder!");
    delay(1000);
    Serial.println("wrong credentials, have to restart the esp32");
    clearEEPROM();
    delay(1000);
    ESP.restart();
    return;
  }

  Serial.println("mDNS responder started");
  // Look for the local IP of the rasbperry pi
  mqttServer = MDNS.queryHost(mqttHostname);

  while (mqttServer.toString() == "0.0.0.0")
  {
    Serial.println("Trying again to resolve mDNS");
    delay(250);
    mqttServer = MDNS.queryHost(mqttHostname);
  }

  Serial.print("IP address of server: ");
  Serial.println(mqttServer.toString());
  // Connect to the MQTT broker
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  while (!client.connected())
  {
    Serial.println("Connecting to MQTT...");
    if (client.connect(DEVICE_ID, mqttUser, mqttPassword))
    {
      Serial.println("connected to the broker");
    }
    else
    {
      /*Serial.print("failed with state ");
        Serial.print(client.state());
        delay(1000);
        Serial.println("wrong credentials, have to restart the esp32");
        clearEEPROM();
        delay(1000);
        ESP.restart();*/
    }
  }
}

void eepromConnection()
{

  //////////WIFI CONNECTION/////////////////////////////////////////
  WiFi.begin(ssid, psw);
  delay(500);
  wifi_timeout = 0;
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to WiFi..");
    wifi_timeout++;
    if (wifi_timeout % 5 == 0)
    {
      Serial.println("\t--> Retry...");
      WiFi.begin(ssid, psw);
    }
  }

  Serial.println("Connected to the WiFi network");

  //////////MQTT CONNECTION/////////////////////////////////////////

  if (!MDNS.begin(DEVICE_ID))
  {
    Serial.println("Error setting up MDNS responder!");
    delay(1000);
    Serial.println("wrong credentials, have to restart the esp32");
    clearEEPROM();
    delay(1000);
    ESP.restart();
    return;
  }

  Serial.println("mDNS responder started");
  // Look for the local IP of the rasbperry pi
  mqttServer = MDNS.queryHost(mqttHostname);

  while (mqttServer.toString() == "0.0.0.0")
  {
    Serial.println("Trying again to resolve mDNS");
    delay(250);
    mqttServer = MDNS.queryHost(mqttHostname);
  }

  Serial.print("IP address of server: ");
  Serial.println(mqttServer.toString());
  // Connect to the MQTT broker
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
  while (!client.connected())
  {
    Serial.println("Connecting to MQTT...");
    if (client.connect(DEVICE_ID, mqttUser, mqttPassword))
    {
      Serial.println("connected to the broker");
    }
    else
    {
      /*Serial.print("failed with state ");
        Serial.print(client.state());
        delay(1000);
        Serial.println("wrong credentials, have to restart the esp32");
        clearEEPROM();
        delay(1000);
        ESP.restart();*/
    }
  }

  /////////////////////////////////////////////////////////////////////

  Serial.println("setup done, everything is connected");
}

void normalConnection()
{
  waitingLowPin();
  testTransmission();

  ssidpsw();
  wifiConnection();
  room();
  mqttConnection();

  Serial.println("setup done, everything is connected");
  SerialBT.end();
  //Serial.println("SerialBT NOT ended");

  EEPROM.writeString(addressone, ssidc); //writes ssid into EEPROM at address 1
  EEPROM.commit();
  Serial.println("ssid written in EEPROM");

  EEPROM.writeString(addresstwo, pswc); //writes psw into EEPROM at address 65 (1+64)
  EEPROM.commit();
  Serial.println("psw written in EEPROM");

  //EEPROM.writeString(addressthree, mqttHostnamec);     //writes hostname in address 129 (65+64)
  //EEPROM.commit();
  //Serial.println("mqttHostname written in EEPROM");

  EEPROM.writeString(addressfour, roomNamec); //writes roomName at address 149 (129+20)
  EEPROM.commit();
  Serial.println("roomName written in EEPROM");

  EEPROM.writeChar(addressfive, roomNamec[roomNamec_index - 1]);
  EEPROM.commit();
  Serial.println("room ID written in EEPROM");

  EEPROM.writeChar(address, 'F'); //writes ack char into EEPROM at address 0
  EEPROM.commit();
  Serial.println("ack char written in EEPROM");
}
