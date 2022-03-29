#include <ESP8266WiFi.h> // wifi library
#include <PubSubClient.h> // mqtt library

#define ECHO_PIN 2
#define TRIG_PIN 16
#define BUFF_LENGTH 5
#define TIME_BETWEEN_READS 100 

float buff[BUFF_LENGTH];
int next = -1;

const int ledPin = 0; 

// WiFi
const char* ssid = "xxxx";
const char* wifi_password = "xxxx";

// MQTT
const char* mqtt_server = "xxxx"; //MQTT Broker IP Address, RPI IP
const char* mqtt_topic = "esp/ultrasonic"; //topic
const char* mqtt_username = "xxxx";
const char* mqtt_password = "xxxx";
const char* clientID = "ESP8266 Micro"; //name of our client

//Creating wifi variables
WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient); // initialize our client 

void callback(char* topic, byte* payload, unsigned int length) {
 Serial.print("Message received :");
 Serial.print(topic);
 for (int i=0;i<length;i++) { //goes through entire message received and checks for 0 or 1
  char receivedChar = (char)payload[i];
  Serial.print(receivedChar);
  if (receivedChar == '0')
  digitalWrite(ledPin, HIGH);
  if (receivedChar == '1')
   digitalWrite(ledPin, LOW); //contrlling LED through mqtt
  }
  Serial.println();
}
bool Connect() {//function to subscribe to topic of ledstatus
  if (client.connect(clientID, mqtt_username, mqtt_password)) {
      Serial.println("Connected to MQTT Broker!");
      client.subscribe("ledStatus");
      return true;
    }
    else {
      Serial.println("Connection to MQTT Broker failed");
      return false;
  }
}
void setup() {
  pinMode(ledPin, OUTPUT); //onboard led
  pinMode(TRIG_PIN, OUTPUT); //ultrasonic trig pin
  pinMode(ECHO_PIN, INPUT); //ultrasonic echo pin
  client.setCallback(callback);

  digitalWrite(ledPin, HIGH);//set led high at start

  Serial.begin(115200);  // Begin Serial on 115200

  WiFi.begin(ssid, wifi_password);// Connect to the WiFi

  if (WiFi.status() != WL_CONNECTED) {//whi
    delay(500);
    Serial.print(".");
  }
  
}

void loop() {
  if (!client.connected()) { //retry connecting
    Connect();
  }
  
  //loop is for receiving messages
  client.loop(); //allows client to be connected to broker, returns false if disconnect

  //ultrasonic function calls
  float distance = readDistance(); //read distance function call
  next = (next >= BUFF_LENGTH || next < 0) ? 0 : (next + 1);
  buff[next] = distance;
  float avg = getAverage(&buff[0], BUFF_LENGTH, 30.0f);
  Serial.println(avg); //getAverage call
  String avgDist = "";
  avgDist = avgDist + avg;
  client.publish("esp/ultrasonic", avgDist.c_str());
  float current_millis = millis();
  while(millis() - current_millis < TIME_BETWEEN_READS)
  { }
  
}
float getAverage(float *buff, int len, float clamp)
{
  float sum = 0;
 
  for(int i = 0; i < len; i++)
  sum += buff[i];

  float ret = sum / len;
  return (ret > clamp) ? clamp : ret;
}

float readDistance()
{
  long duration;
  long current_micros = micros();

  digitalWrite(TRIG_PIN, HIGH);

  while(micros() - current_micros < 10)
  { }
 
  digitalWrite(TRIG_PIN, LOW);
 
  duration = pulseIn(ECHO_PIN, HIGH);
  return duration * 0.034f / 2.0f; // count half distance
}
