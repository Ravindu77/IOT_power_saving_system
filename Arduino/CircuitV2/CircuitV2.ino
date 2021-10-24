#include <dht_nonblocking.h>
#define DHT_SENSOR_TYPE DHT_TYPE_11

const int buttonPin = 2;
const int add = 10, minus = 11;
const int RLed = 3, GLed = 4, YLed = 5;
int buttonState;
int addState, minusState;
bool pushB;

bool ac, heater;

const int DHT_SENSOR_PIN = 8;
DHT_nonblocking dht_sensor( DHT_SENSOR_PIN, DHT_SENSOR_TYPE );

float temperature;
float humidity;
float idealTemp;

void setup() {
  buttonState = 0;
  addState = 0;
  minusState = 0;

  ac = false;
  heater = false;
  
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

  readTempHumid();
  pushButton(buttonState, buttonPin);
  
  tempChange();
  if(pushB){
    LedOn(YLed);
    tempControl();
  }else{
    allOff();
    blinkY();
  }
  
}

void tempControl(){
  //delay(1000);
  if(( idealTemp < temperature)){
    heaterOn();
  }
  if( idealTemp > temperature){
    acOn();
  }
  if(idealTemp == temperature){
    allOff();
  }
}

void acOn(){
  if(heater){
    heaterOff();
  }
  if(ac){
    LedOn(GLed);
  }else{
    ac = true;
    LedOn(GLed);
  }
}

void acOff(){
  if(ac){
    ac = false;
    LedOff(GLed);
  }else{
    LedOff(GLed);
  }
}

void heaterOn(){
  if(ac){
    acOff();
  }
  if(heater){
    LedOn(RLed);
  }else{
    heater = true;
    LedOn(RLed);
  }
}

void heaterOff(){
  if(heater){
    heater = false;
    LedOff(RLed);
  }else{
    LedOff(RLed);
  }
}

void allOff(){
  acOff();
  heaterOff();
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
    Serial.print( "Temp: " );
    Serial.print( temperature, 1 );
    Serial.print( " " );
    Serial.print( "Humid: " );
    Serial.print( humidity, 1 );
    Serial.println("%");
  }
}
