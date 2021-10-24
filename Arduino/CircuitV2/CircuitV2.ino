#include <dht_nonblocking.h>
#define DHT_SENSOR_TYPE DHT_TYPE_11

const int buttonPin = 2;
const int add = 10, minus = 11;
const int RLed = 3, GLed = 4, YLed = 5;
int buttonState;
int addState, minusState;
bool pushB;

const int DHT_SENSOR_PIN = 8;
DHT_nonblocking dht_sensor( DHT_SENSOR_PIN, DHT_SENSOR_TYPE );

float temperature;
float humidity;
float idealTemp;

void setup() {
  buttonState = 0;
  addState = 0;
  minusState = 0;
  
  idealTemp = 25;
  pushB = false;
  Serial.begin(9600);
  pinMode(buttonPin, INPUT);
  pinMode(add, INPUT);
  pinMode(minus, INPUT);
  pinMode(RLed, OUTPUT);
  pinMode(GLed, OUTPUT);
  pinMode(YLed, OUTPUT);

}

void loop() {
  buttonState = 0;
  addState = 0;
  minusState = 0;
  
  pushButton(buttonState, buttonPin);
  tempChange();

  if(pushB){
    LedOn(YLed);
    readTempHumid();
  }else{
    allOff();
    blinkY();
  }
  
}


void tempChange(){
  if(button(addState, add)){
    delay(500);
    if(idealTemp < 40){
      idealTemp++;
    }
    Serial.println(idealTemp);
  }
  if(button(minusState, minus)){
    delay(500);
    if(idealTemp > 10){
      idealTemp--;
    }
    Serial.println(idealTemp);
  }
}

void blinkY(){
  LedOn(YLed);
  delay(300);
  LedOff(YLed);
  delay(300);
}

void allOff(){
  LedOff(RLed);
  LedOff(GLed);
}

void pushButton(int state, int pin){
  if(button(state, pin)){
    if(pushB){
      pushB = false;
      Serial.print("Off \n");
      delay(500);
    }else{
      pushB = true;
      Serial.print("On \n");
      delay(500);
    }
  }
}

//Function Button
bool button(int state, int pin){
  state = digitalRead(pin);
  if (state == HIGH) {
    return true;
  } else{
    return false;
  }
}

void LedOn(int led){
  digitalWrite(led, HIGH);
}

void LedOff(int led){
  digitalWrite(led, LOW);
}

void readTempHumid(){
  //dht_sensor.measure(&temperature, &humidity);
  if(dht_sensor.measure(&temperature, &humidity)){
    Serial.print( idealTemp, 1 );
    Serial.print( " " );
    Serial.print( temperature, 1 );
    Serial.print( " " );
    Serial.print( humidity, 1 );
    Serial.println();
  }
}
