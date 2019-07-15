#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiClient.h>
#include "PubSubClient.h"
#include "BluetoothSerial.h"
#include "EEPROM.h"
#include <alloca.h>
#include <string>
#include <cstring>
#include <string.h>
#include "ArduinoJson.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

#define EEPROM_SIZE 256

#define interruptPin 25 //Digital pin connected to the push button
#define rele_one 23
#define rele_two 22
#define rele_three 21
#define rele_four 19
#define rele_five 18
#define rele_six 17
#define rele_seven 16
#define rele_eight 15

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
int addressvalves = 200;
//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

/* MQTT broker connection credentials */
const char *DEVICE_ID = "DEV00";
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

/*char used in BT transmission*/
char termo[] = ":termo";
char test_transmission[20];

int passwordc_index = 0;
int ssidc_index = 0;
int test_index = 0;
int wifi_timeout = 0;
int roomNamec_index = 0;

int roomToValve[8];

// Device ID, change this for each ESP you are going to flash
char ESPname[] = "2";
char ack_char = '@';
char no_ack_char = '#';
char roomIDc;
char testc;

String start_control = "\"actuator\" : \"";
String end_control = "\"";
String mqtt_config_actuator_control = "";

/* Stupid mechanism to wait time without stopping the cpu */
int start_time;
const int time_interval = 5000;

WiFiClient espClient;
PubSubClient client(espClient);
BluetoothSerial SerialBT;

///////////////////////////////////////////////////////////////////
void showCredentials()
{
  //taking the credentials from EEPROM
  testc = EEPROM.readChar(address);
  EEPROM.readString(addressone).toCharArray(ssidc, 64);
  EEPROM.readString(addresstwo).toCharArray(passwordc, 64);
  //EEPROM.readString(addressthree).toCharArray(mqttHostnamec,20);
  EEPROM.readString(addressfour).toCharArray(roomNamec, 20);
  roomIDc = EEPROM.readChar(addressfive);

  roomToValve[0] = EEPROM.readInt(addressvalves);
  roomToValve[1] = EEPROM.readInt(addressvalves + 4);
  roomToValve[2] = EEPROM.readInt(addressvalves + 8);
  roomToValve[3] = EEPROM.readInt(addressvalves + 12);
  roomToValve[4] = EEPROM.readInt(addressvalves + 16);
  roomToValve[5] = EEPROM.readInt(addressvalves + 20);
  roomToValve[6] = EEPROM.readInt(addressvalves + 24);
  roomToValve[7] = EEPROM.readInt(addressvalves + 28);

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

  Serial.print("valve of room 1 is ");
  Serial.println(roomToValve[0]);
  Serial.print("valve of room 2 is ");
  Serial.println(roomToValve[1]);
  Serial.print("valve of room 3 is ");
  Serial.println(roomToValve[2]);
  Serial.print("valve of room 4 is ");
  Serial.println(roomToValve[3]);
  Serial.print("valve of room 5 is ");
  Serial.println(roomToValve[4]);
  Serial.print("valve of room 6 is ");
  Serial.println(roomToValve[5]);
  Serial.print("valve of room 7 is ");
  Serial.println(roomToValve[6]);
  Serial.print("valve of room 8 is ");
  Serial.println(roomToValve[7]);
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
}

int correspondance(int pos)
{
  switch (pos)
  {
  case 1:
    return rele_one;
    break;
  case 2:
    return rele_two;
    break;
  case 3:
    return rele_three;
    break;
  case 4:
    return rele_four;
    break;
  case 5:
    return rele_five;
    break;
  case 6:
    return rele_six;
    break;
  case 7:
    return rele_seven;
    break;
  case 8:
    return rele_eight;
    break;
  }
}

void reSubHotTopic()
{
  if ((EEPROM.readInt(addressvalves)))
  {
    if (client.subscribe("actuator/hot/1") == false)
    {
      Serial.println("not subscribed to actuator/hot/1 topic");
    }
    Serial.println("Subscribed to actuator/hot/1 topic");
  }

  if ((EEPROM.readInt(addressvalves + 4)))
  {
    if (client.subscribe("actuator/hot/2") == false)
    {
      Serial.println("not subscribed to actuator/hot/2 topic");
    }
    Serial.println("Subscribed to actuator/hot/2 topic");
  }

  if ((EEPROM.readInt(addressvalves + 8)))
  {
    if (client.subscribe("actuator/hot/3") == false)
    {
      Serial.println("not subscribed to actuator/hot/3 topic");
    }
    Serial.println("Subscribed to actuator/hot/3 topic");
  }

  if ((EEPROM.readInt(addressvalves + 12)))
  {
    if (client.subscribe("actuator/hot/4") == false)
    {
      Serial.println("not subscribed to actuator/hot/4 topic");
    }
    Serial.println("Subscribed to actuator/hot/4 topic");
  }

  if ((EEPROM.readInt(addressvalves + 16)))
  {
    if (client.subscribe("actuator/hot/5") == false)
    {
      Serial.println("not subscribed to actuator/hot/5 topic");
    }
    Serial.println("Subscribed to actuator/hot/5 topic");
  }

  if ((EEPROM.readInt(addressvalves + 20)))
  {
    if (client.subscribe("actuator/hot/6") == false)
    {
      Serial.println("not subscribed to actuator/hot/6 topic");
    }
    Serial.println("Subscribed to actuator/hot/6 topic");
  }

  if ((EEPROM.readInt(addressvalves + 24)))
  {
    if (client.subscribe("actuator/hot/7") == false)
    {
      Serial.println("not subscribed to actuator/hot/7 topic");
    }
    Serial.println("Subscribed to actuator/hot/7 topic");
  }

  if ((EEPROM.readInt(addressvalves + 28)))
  {
    if (client.subscribe("actuator/hot/8") == false)
    {
      Serial.println("not subscribed to actuator/hot/8 topic");
    }
    Serial.println("Subscribed to actuator/hot/8 topic");
  }
}
////////////////////////////////////////////////////////////////////////

void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  String messageTemp;

  for (int i = 0; i < length; i++)
  {
    //Serial.print((char)payload[i]);
    messageTemp += (char)payload[i];
  }
  Serial.println(messageTemp.c_str());
  Serial.println();
  Serial.println("-----------------------");

  if (String(topic) == "actuator/configuration")
  {
    int messageLenght = messageTemp.length();
    StaticJsonDocument<200> doc;
    char json[messageLenght + 1];
    Serial.print("message lenght is ");
    Serial.println(messageLenght);
    strcpy(json, messageTemp.c_str());
    Serial.print("char json[messageLenght] is ");
    Serial.println(json);

    DeserializationError error = deserializeJson(doc, json);
    if (error)
    {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.c_str());
      return;
    }

    const char *room = doc["room"];
    const char *actuator = doc["actuator"];
    const char *valve = doc["valve"];

    Serial.print("room char* is ");
    Serial.println(room);
    Serial.print("actuator char* is ");
    Serial.println(actuator);
    Serial.print("valve char* is ");
    Serial.println(valve);

    if (actuator[0] == roomIDc)
    {
      int vectorPosition = (room[0] - '0') - 1;
      Serial.print("the vector position is ");
      Serial.println(vectorPosition);
      roomToValve[vectorPosition] = valve[0] - '0';
      Serial.print("the roomToValve vector is ");
      Serial.println(roomToValve[vectorPosition]);
      String topic = "actuator/hot/";
      topic += room;
      Serial.print("the topic name is ");
      Serial.println(topic.c_str());
      if (client.subscribe(topic.c_str()) == false)
      {
        Serial.println("failed to subscribe to the topic");
      }
      Serial.println("subscribed to the topic");

      Serial.println("writing the valve in EEPROM");
      EEPROM.writeInt(addressvalves + (vectorPosition * 4), roomToValve[vectorPosition]); // -2^31
      Serial.println(EEPROM.readInt(addressvalves + (vectorPosition * 4)));
      EEPROM.commit();
      Serial.println("valve written in EEPROM");
    }
  }

  if (String(topic) == "actuator/hot/1")
  {
    Serial.println("received message in topic actuator/hot/1");
    int relePin = correspondance(roomToValve[0]);
    Serial.print("relePin is ");
    Serial.println(relePin);

    if (messageTemp == "{\"cmd\": \"ON\"}")
    {
      Serial.println("Rele ON");
      digitalWrite(relePin, HIGH);
    }
    else if (messageTemp == "{\"cmd\": \"OFF\"}")
    {
      Serial.println("Rele OFF");
      digitalWrite(relePin, LOW);
    }
  }

  if (String(topic) == "actuator/hot/2")
  {
    Serial.println("received message in topic actuator/hot/2");
    int relePin = correspondance(roomToValve[1]);
    Serial.print("relePin is ");
    Serial.println(relePin);

    if (messageTemp == "{\"cmd\": \"ON\"}")
    {
      Serial.println("Rele ON");
      digitalWrite(relePin, HIGH);
    }
    else if (messageTemp == "{\"cmd\": \"OFF\"}")
    {
      Serial.println("Rele OFF");
      digitalWrite(relePin, LOW);
    }
  }

  if (String(topic) == "actuator/hot/3")
  {
    Serial.println("received message in topic actuator/hot/3");
    int relePin = correspondance(roomToValve[2]);
    Serial.print("relePin is ");
    Serial.println(relePin);

    if (messageTemp == "{\"cmd\": \"ON\"}")
    {
      Serial.println("Rele ON");
      digitalWrite(relePin, HIGH);
    }
    else if (messageTemp == "{\"cmd\": \"OFF\"}")
    {
      Serial.println("Rele OFF");
      digitalWrite(relePin, LOW);
    }
  }

  if (String(topic) == "actuator/hot/4")
  {
    Serial.println("received message in topic actuator/hot/4");
    int relePin = correspondance(roomToValve[3]);
    Serial.print("relePin is ");
    Serial.println(relePin);

    if (messageTemp == "{\"cmd\": \"ON\"}")
    {
      Serial.println("Rele ON");
      digitalWrite(relePin, HIGH);
    }
    else if (messageTemp == "{\"cmd\": \"OFF\"}")
    {
      Serial.println("Rele OFF");
      digitalWrite(relePin, LOW);
    }
  }

  if (String(topic) == "actuator/hot/5")
  {
    Serial.println("received message in topic actuator/hot/5");
    int relePin = correspondance(roomToValve[4]);
    Serial.print("relePin is ");
    Serial.println(relePin);

    if (messageTemp == "{\"cmd\": \"ON\"}")
    {
      Serial.println("Rele ON");
      digitalWrite(relePin, HIGH);
    }
    else if (messageTemp == "{\"cmd\": \"OFF\"}")
    {
      Serial.println("Rele OFF");
      digitalWrite(relePin, LOW);
    }
  }

  if (String(topic) == "actuator/hot/6")
  {
    Serial.println("received message in topic actuator/hot/6");
    int relePin = correspondance(roomToValve[5]);
    Serial.print("relePin is ");
    Serial.println(relePin);

    if (messageTemp == "{\"cmd\": \"ON\"}")
    {
      Serial.println("Rele ON");
      digitalWrite(relePin, HIGH);
    }
    else if (messageTemp == "{\"cmd\": \"OFF\"}")
    {
      Serial.println("Rele OFF");
      digitalWrite(relePin, LOW);
    }
  }

  if (String(topic) == "actuator/hot/7")
  {
    Serial.println("received message in topic actuator/hot/7");
    int relePin = correspondance(roomToValve[6]);
    Serial.print("relePin is ");
    Serial.println(relePin);

    if (messageTemp == "{\"cmd\": \"ON\"}")
    {
      Serial.println("Rele ON");
      digitalWrite(relePin, HIGH);
    }
    else if (messageTemp == "{\"cmd\": \"OFF\"}")
    {
      Serial.println("Rele OFF");
      digitalWrite(relePin, LOW);
    }
  }

  if (String(topic) == "actuator/hot/8")
  {
    Serial.println("received message in topic actuator/hot/8");
    int relePin = correspondance(roomToValve[7]);
    Serial.print("relePin is ");
    Serial.println(relePin);

    if (messageTemp == "{\"cmd\": \"ON\"}")
    {
      Serial.println("Rele ON");
      digitalWrite(relePin, HIGH);
    }
    else if (messageTemp == "{\"cmd\": \"OFF\"}")
    {
      Serial.println("Rele OFF");
      digitalWrite(relePin, LOW);
    }
  }

  Serial.println("-----------------------");
}

void setup()
{
  /* Init serial communication for debug purposes */
  Serial.begin(115200);

  pinMode(interruptPin, INPUT_PULLUP);

  pinMode(rele_one, OUTPUT);
  pinMode(rele_two, OUTPUT);
  pinMode(rele_three, OUTPUT);
  pinMode(rele_four, OUTPUT);
  pinMode(rele_five, OUTPUT);
  pinMode(rele_six, OUTPUT);
  pinMode(rele_seven, OUTPUT);
  pinMode(rele_eight, OUTPUT);

  Serial.println("before initializing EEPROM");

  if (!EEPROM.begin(EEPROM_SIZE))
  {
    Serial.println("Failed to initialise EEPROM");
    Serial.println("Restarting...");
    delay(1000);
    ESP.restart();
  }

  Serial.println("after initializing EEPROM");

  // clearEEPROM();

  if (EEPROM.readChar(address) == 'F')
  { //ack char for credentials
    //credentials already stored in eeprom
    Serial.println("eeprom connection in if {}");
    showCredentials();
    eepromConnection();
    reSubHotTopic();
  }
  else
  {
    //credentials not yet stored in eeprom
    Serial.println("normal connection in else {}");
    normalConnection();
  }

  if (client.subscribe("actuator/configuration") == false)
  {
    Serial.println("not subscribed to actuator/configuration topic");
  }
  Serial.println("Subscribed to actuator/configuration topic");

  start_time = millis();
}

void loop()
{
  if (!client.connected())
  {
    Serial.println("client not connected");
    //ESP.restart();
    reconnect();

    if (client.subscribe("actuator/configuration") == false)
    {
      Serial.println("not subscribed to actuator/config topic");
    }
    Serial.println("Subscribed to actuator/configiguration topic");

    reSubHotTopic();

    Serial.println("valve corrispondance is");
    Serial.print(roomToValve[0]);
    Serial.print(roomToValve[1]);
    Serial.print(roomToValve[2]);
    Serial.print(roomToValve[3]);
    Serial.print(roomToValve[4]);
    Serial.print(roomToValve[5]);
    Serial.print(roomToValve[6]);
    Serial.print(roomToValve[7]);
  }

  if (millis() - start_time > time_interval)
  {
    Serial.println("millis reset");
    start_time = millis();
  }
  client.loop();
}

//room  1  valve  8
//room  2  valve  7
//room  3  valve  6
//room  4  valve  5
//room  5  valve  4
//room  6  valve  3
//room  7  valve  2
//room  8  valve  1
