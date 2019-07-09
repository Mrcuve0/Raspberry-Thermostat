#include "BluetoothSerial.h"
#include <WiFi.h>
#include "PubSubClient.h"
#include <ESPmDNS.h>
#include <WiFiClient.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

#define interruptPin 25 //Digital pin connected to the push button
#define rele_one 23
#define rele_two 22
#define rele_three 21
#define rele_four 19
#define rele_five 18
#define rele_six 17
#define rele_seven 16
#define rele_eight 15

const char *DEVICE_ID = "DEV00";
const int mqttPort = 1883;
const char *mqttUser = "";
const char *mqttPassword = "";
IPAddress mqttServer;

char termo[] = ":termo";
char test_transmission[20];

char ssidc[64] = "";
char pswc[64] = "";
char mqttHostnamec[20] = "";
char roomNamec[20] = "";

char *ssid = ssidc;
char *psw = pswc;
char *mqttHostname = mqttHostnamec;

int pswc_index = 0;
int ssidc_index = 0;
int mqttHostnamec_index = 0;
int test_index = 0;
int wifi_timeout = 0;

// Device ID, change this for each ESP you are going to flash
char ESPname[] = "Actuator 1";
char ack_char = '@';
char no_ack_char = '#';

/* Stupid mechanism to wait time without stopping the cpu */
int start_time;
const int time_interval = 5000;

WiFiClient espClient;
PubSubClient client(espClient);
BluetoothSerial SerialBT;

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

  //topic rele/IDattuatore/numeroRele
  
  /*topic one*/
  if (String(topic) == "rele/IDatt/1")
  {
    Serial.println("mqtt message recieved on topic one");
    if (messageTemp == "ON")
    {
      Serial.println("Rele_one ON");
      digitalWrite(rele_one, HIGH);
    }
    else if (messageTemp == "OFF")
    {
      Serial.println("Rele_one OFF");
      digitalWrite(rele_one, LOW);
    }
  }
  /*topic two*/
  if (String(topic) == "rele/IDatt/2")
  {
    Serial.println("mqtt message recieved on topic two");
    if (messageTemp == "ON")
    {
      Serial.println("Rele_two ON");
      digitalWrite(rele_two, HIGH);
    }
    else if (messageTemp == "OFF")
    {
      Serial.println("Rele_two OFF");
      digitalWrite(rele_two, LOW);
    }
  }
  /*topic three*/
  if (String(topic) == "rele/IDatt/3")
  {
    Serial.println("mqtt message recieved on topic three");
    if (messageTemp == "ON")
    {
      Serial.println("Rele_three ON");
      digitalWrite(rele_three, HIGH);
    }
    else if (messageTemp == "OFF")
    {
      Serial.println("Rele_three OFF");
      digitalWrite(rele_three, LOW);
    }
  }
  /*topic four*/
  if (String(topic) == "rele/IDatt/4")
  {
    Serial.println("mqtt message recieved on topic four");
    if (messageTemp == "ON")
    {
      Serial.println("Rele_four ON");
      digitalWrite(rele_four, HIGH);
    }
    else if (messageTemp == "OFF")
    {
      Serial.println("Rele_four OFF");
      digitalWrite(rele_four, LOW);
    }
  }
  /*topic five*/
  if (String(topic) == "rele/IDatt/5")
  {
    Serial.println("mqtt message recieved on topic five");
    if (messageTemp == "ON")
    {
      Serial.println("Rele_five ON");
      digitalWrite(rele_five, HIGH);
    }
    else if (messageTemp == "OFF")
    {
      Serial.println("Rele_five OFF");
      digitalWrite(rele_five, LOW);
    }
  }
  /*topic six*/
  if (String(topic) == "rele/IDatt/6")
  {
    Serial.println("mqtt message recieved on topic six");
    if (messageTemp == "ON")
    {
      Serial.println("Rele_six ON");
      digitalWrite(rele_six, HIGH);
    }
    else if (messageTemp == "OFF")
    {
      Serial.println("Rele_six OFF");
      digitalWrite(rele_six, LOW);
    }
  }
  /*topic seven*/
  if (String(topic) == "rele/IDatt/7")
  {
    Serial.println("mqtt message recieved on topic seven");
    if (messageTemp == "ON")
    {
      Serial.println("Rele_seven ON");
      digitalWrite(rele_seven, HIGH);
    }
    else if (messageTemp == "OFF")
    {
      Serial.println("Rele_seven OFF");
      digitalWrite(rele_seven, LOW);
    }
  }
  /*topic eight*/
  if (String(topic) == "rele/IDatt/8")
  {
    Serial.println("mqtt message recieved on topic eight");
    if (messageTemp == "ON")
    {
      Serial.println("Rele_eight ON");
      digitalWrite(rele_eight, HIGH);
    }
    else if (messageTemp == "OFF")
    {
      Serial.println("Rele_eight OFF");
      digitalWrite(rele_eight, LOW);
    }
  }
}

void setup()
{
  Serial.begin(115200);
  pinMode(interruptPin, INPUT_PULLUP);
  SerialBT.begin(ESPname); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
  client.setCallback(callback);
  pinMode(rele_one, OUTPUT);
  pinMode(rele_two, OUTPUT);
  pinMode(rele_three, OUTPUT);
  pinMode(rele_four, OUTPUT);
  pinMode(rele_five, OUTPUT);
  pinMode(rele_six, OUTPUT);
  pinMode(rele_seven, OUTPUT);
  pinMode(rele_eight, OUTPUT);
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

  Serial.println("setup done, everything is connected");
  // SerialBT.end();
  Serial.println("SerialBT NOT ended");
  /*subscribe to 8 topic, we have 8 rele*/
  client.subscribe("rele/IDatt/1");
  client.subscribe("rele/IDatt/2");
  client.subscribe("rele/IDatt/3");
  client.subscribe("rele/IDatt/4");
  client.subscribe("rele/IDatt/5");
  client.subscribe("rele/IDatt/6");
  client.subscribe("rele/IDatt/7");
  client.subscribe("rele/IDatt/8");

  start_time = millis();
  Serial.println("initialized the start time");
}

void loop()
{
  if (millis() - start_time > time_interval)
  {
    start_time = millis();
  }
}
