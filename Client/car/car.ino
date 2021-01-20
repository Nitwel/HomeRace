#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Servo.h>
#include <Regexp.h>
 
const char* SSID = "FRITZ!Box 7362 SL";
const char* PSK = "86619567583490915352";
const char* MQTT_BROKER = "192.168.0.47";

int FORWARD_WHEEL = D0;
int BACKWARD_WHEEL = D1;
int STEERING = D2;
int SPEED_WHEEL = D3;

Servo myservo;
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
 
void setup() {
    pinMode(FORWARD_WHEEL, OUTPUT);
    pinMode(BACKWARD_WHEEL, OUTPUT);
    
    Serial.begin(115200);
    setup_wifi();
    client.setServer(MQTT_BROKER, 1883);
    client.setCallback(callback);
    myservo.attach(STEERING);
}
 
void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(SSID);
 
    WiFi.begin(SSID, PSK);
 
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
 
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}
 
void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Received message [");
    Serial.print(topic);
    Serial.print("] ");
    
    char msg[length+1];
    for (int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
        msg[i] = (char)payload[i];
    }
    Serial.println();
 
    msg[length] = '\0';

    if(strcmp(topic, "/drive") == 0) {
      Serial.println("Driving");
      signed char speed = msg[0];
      signed char direction = msg[1];

      int speed_real = speed / 100.0 * 255;
      int degree = (((int) -direction) + 100) / 201.0 * 180;

      Serial.println(speed_real);

      if(speed > 0) {
        digitalWrite(FORWARD_WHEEL,HIGH);
        digitalWrite(BACKWARD_WHEEL,LOW);
        analogWrite(SPEED_WHEEL, speed_real);
      } else if(speed == 0) {
        digitalWrite(FORWARD_WHEEL,LOW);
        digitalWrite(BACKWARD_WHEEL,LOW);
        analogWrite(SPEED_WHEEL, 0);
        
      } else {
        digitalWrite(FORWARD_WHEEL,LOW);
        digitalWrite(BACKWARD_WHEEL,HIGH);
        analogWrite(SPEED_WHEEL, -speed_real);
      }
      myservo.write(degree);
      
    }

    MatchState ms;
    ms.Target(msg);
    if(char result = ms.Match("ping") == REGEXP_MATCHED){
      client.publish("/home/data", "pong");
    }

    if(ms.Match("stop") == REGEXP_MATCHED){
      Serial.println("stopping");
      digitalWrite(FORWARD_WHEEL,LOW);
      digitalWrite(BACKWARD_WHEEL,LOW);
    }

    if(char result = ms.Match("forward") == REGEXP_MATCHED){
      Serial.println("Going forward");
      digitalWrite(FORWARD_WHEEL,HIGH);
      digitalWrite(BACKWARD_WHEEL,LOW);
    }

    if(char result = ms.Match("backward") == REGEXP_MATCHED){
      Serial.println("Going backward");
      digitalWrite(FORWARD_WHEEL,LOW);
      digitalWrite(BACKWARD_WHEEL,HIGH);
    }

    if(char result = ms.Match("left (%d%d%d)") == REGEXP_MATCHED){
      Serial.println("Going backward");
      int degree = String(ms.GetCapture(msg, 0)).toInt();
      Serial.println(degree);
      myservo.write(degree);
    }
}
 
void reconnect() {
    while (!client.connected()) {
        Serial.println("Reconnecting MQTT...");
        if (!client.connect("ESP8266Client", "race", "race")) {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" retrying in 5 seconds");
            delay(5000);
        }
    }
    client.subscribe("/home/data");
    client.subscribe("/drive");
    
    Serial.println("MQTT Connected...");
}
 
void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
}
