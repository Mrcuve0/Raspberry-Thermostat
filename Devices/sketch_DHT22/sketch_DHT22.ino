#include <Adafruit_Sensor.h>
#include <DHT.h>

#define DHTPIN 27     // Digital pin connected to the DHT sensor

// Uncomment the type of sensor in use:
//#define DHTTYPE    DHT11     // DHT 11
#define DHTTYPE    DHT22     // DHT 22 (AM2302)
//#define DHTTYPE    DHT21     // DHT 21 (AM2301)

DHT dht(DHTPIN, DHTTYPE);



void setup(){
  // Serial port for debugging purposes
  Serial.begin(115200);

  dht.begin();

}
 
void loop(){
  float t = dht.readTemperature();
  float h = dht.readHumidity();

  Serial.print("temperature ");
  Serial.print(t);
  Serial.print("\n");
  Serial.print("humidity ");
  Serial.print(h);
  Serial.print("\n");
  
  delay(5000);
}
