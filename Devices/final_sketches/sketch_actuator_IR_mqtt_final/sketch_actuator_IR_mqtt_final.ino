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

#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiClient.h>
#include "PubSubClient.h"
#include "BluetoothSerial.h"
#include "EEPROM.h"
#include "IRremote.h"
#include <alloca.h>
#include <string>
#include <cstring>
#include <string.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

#define EEPROM_SIZE 256

#define interruptPin 25 //Digital pin connected to the push button
#define resetPin 26
#define greenLed 33 //used for BT transmission
#define redLed 32   //used for IR code
#define blueLed 35  //used for reconnection

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

/* MQTT broker connection credentials */
const char *DEVICE_ID = "DEV02";
const int mqttPort = 1883;
IPAddress mqttServer;
const char *mqttUser = "";
const char *mqttPassword = "";

char ssidc[64] = "";
char passwordc[64] = "";
char roomNamec[20] = "";

/* Wifi connection credentials */

char *ssid = ssidc;
char *password = passwordc;
char *roomName = roomNamec;
char *mqttHostname = "thermostat";
char *airConditioningTopic = "actuator/cold/";

/*char used in BT transmission*/
char termo[] = ":termo";
char test_transmission[20];

int passwordc_index = 0;
int ssidc_index = 0;
int test_index = 0;
int wifi_timeout = 0;
int roomNamec_index = 0;

int state = 0;

// Device ID, change this for each ESP you are going to flash
char ESPname[] = "6";
char ack_char = '@';
char no_ack_char = '#';
char roomIDc;
char testc;

/* Stupid mechanism to wait time without stopping the cpu */
int start_time;
const int time_interval = 5000;

//stuff for IR functionalities///////////
int RECV_PIN = 15;
unsigned long code = 50; //default code
IRrecv irrecv(RECV_PIN);
IRsend irsend;
decode_results results;

WiFiClient espClient;
PubSubClient client(espClient);
BluetoothSerial SerialBT;

void IRAM_ATTR handleInterrupt();

void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++)
  {
    //Serial.print((char)payload[i]);
    messageTemp += (char)payload[i];
  }
  Serial.println(messageTemp.c_str());
  Serial.println("-----------------------");

  Serial.print("state is ");
  Serial.println(state);
  Serial.println("-----------------------");

  Serial.print("airconditioningtopic is ");
  Serial.println(airConditioningTopic);
  Serial.println("-----------------------");

  if (String(topic) == String(airConditioningTopic))
  {
    Serial.println("in actuator/cold/X");
    if (messageTemp == "{\"cmd\": \"ON\"}")
    {
      Serial.println("compare ON successful");
      if (!state)
      {
        Serial.println("message ON received");
        irsend.sendSony(0xa90, 12);
        Serial.println("sony command ON sent");
        state = 1;
      }
    }
    if (messageTemp == "{\"cmd\": \"OFF\"}")
    {
      Serial.println("compare OFF successful");
      if (state)
      {
        Serial.println("message OFF received");
        irsend.sendSony(0xa90, 12);
        Serial.println("sony command OFF sent");
        state = 0;
      }
    }
  }
  Serial.println("-----------------------");
  /*EEPROM.write(addressbool, state);
  EEPROM.commit();
  Serial.println("state written in EEPROM");
  Serial.println("-----------------------");
  */
}

void setup()
{
  /* Init serial communication for debug purposes */
  Serial.begin(115200);
  pinMode(interruptPin, INPUT_PULLUP);
  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);
  pinMode(blueLed, OUTPUT);
  pinMode(resetPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(resetPin), handleInterrupt, FALLING);

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
    airTopicAttach();
  }
  else
  {
    //credentials not yet stored in eeprom
    Serial.println("normal connection in else {}");
    digitalWrite(blueLed, HIGH);
    normalConnection();
    digitalWrite(blueLed, LOW);
    airTopicAttach();
  }

  newIRcode();

  if (client.subscribe(airConditioningTopic) == false)
  {
    Serial.println("not subscribed to test topic");
  }
  Serial.println("Subscribed to airconditioning topic");
  Serial.print("topic name is ");
  Serial.println(airConditioningTopic);

  start_time = millis();
}

void loop()
{
  if (!client.connected())
  {
    Serial.println("client not connected");
    //ESP.restart();
    digitalWrite(blueLed, HIGH);
    reconnect();
    digitalWrite(blueLed, LOW);
    //showCredentials();
    //airTopicAttach();
    if (client.subscribe(airConditioningTopic) == false)
    {
      Serial.println("not subscribed to test topic");
    }
    Serial.println("Subscribed to airconditioning topic");
    Serial.print("topic name is ");
    Serial.println(airConditioningTopic);
  }

  if (millis() - start_time > time_interval)
  {
    //client.publish(airConditioningTopic , "ON");
    start_time = millis();
    Serial.println("millis reset");
  }
  client.loop();
}

///////////////////////////////////////////////////////////////////
void IRAM_ATTR handleInterrupt()
{
  Serial.println("reset button pressed");
  delay(1000);
  clearEEPROM();
  ESP.restart();
}

void newIRcode()
{
  Serial.println("looking for a new IR code");
  digitalWrite(redLed, HIGH);
  irrecv.enableIRIn(); // Start the receiver
  Serial.println("IR enabled");
  while (digitalRead(interruptPin) == HIGH)
  {
    if (irrecv.decode(&results))
    {
      Serial.println("IR code received");
      code = results.value;
      break;
    }
  }
  Serial.print("code is ");
  Serial.println(code, HEX);
  Serial.println("IR setup done");
  digitalWrite(redLed, LOW);
}

char *appendCharToCharArray(char *array, char a)
{
  size_t len = strlen(array);
  char *ret = new char[len + 2];
  strcpy(ret, array);
  ret[len] = a;
  ret[len + 1] = '\0';
  return ret;
}

void airTopicAttach()
{
  Serial.print("room ID is ");
  Serial.println(roomIDc);
  airConditioningTopic = appendCharToCharArray(airConditioningTopic, roomIDc);
  Serial.print("the airconditioning topic is ");
  Serial.println(airConditioningTopic);
}

void showCredentials()
{
  //taking the credentials from EEPROM
  testc = EEPROM.readChar(address);
  EEPROM.readString(addressone).toCharArray(ssidc, 64);
  EEPROM.readString(addresstwo).toCharArray(passwordc, 64);
  //EEPROM.readString(addressthree).toCharArray(mqttHostnamec,20);
  EEPROM.readString(addressfour).toCharArray(roomNamec, 20);
  roomIDc = EEPROM.readChar(addressfive);

  //printing the credentials from EEPROM
  Serial.print("test is ");
  Serial.println(testc);
  Serial.print("ssid is ");
  Serial.println(ssidc);
  Serial.print("psw is ");
  Serial.println(passwordc);
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

void eepromConnection()
{

  //////////WIFI CONNECTION/////////////////////////////////////////
  WiFi.begin(ssid, password);
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
      WiFi.begin(ssid, password);
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

  EEPROM.writeString(addressone, ssidc); //writes ssid into EEPROM at address 1
  EEPROM.commit();
  Serial.println("ssid written in EEPROM");

  EEPROM.writeString(addresstwo, passwordc); //writes psw into EEPROM at address 65 (1+64)
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
    passwordc[passwordc_index] = SerialBT.read();
    Serial.println(passwordc[passwordc_index]);
    passwordc_index++;
    delay(40);
  }
  Serial.println(passwordc_index);
  passwordc[strlen(passwordc)] = '\0';
  Serial.println(password);
}

void wifiConnection()
{
  WiFi.begin(ssid, password);
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
      WiFi.begin(ssid, password);
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
  Serial.println(roomName);
  Serial.print("roomID is ");
  roomIDc = roomNamec[roomNamec_index - 1];
  Serial.println(roomIDc);
  SerialBT.write(ack_char);
  Serial.println("sent the ack char for roomName");
  delay(1000);
  SerialBT.end();
  Serial.println("BT ended");
}

void reconnect()
{

  //////////WIFI CONNECTION/////////////////////////////////////////
  Serial.println("before wifi.begin");
  if (WiFi.status() != WL_CONNECTED)
  {
    WiFi.begin(ssid, password);
    Serial.println("after first wifi.begin");
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
        WiFi.begin(ssid, password);
      }
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
