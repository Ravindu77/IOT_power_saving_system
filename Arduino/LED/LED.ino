const int RLed = 3, GLed = 4, YLed = 5;
void setup() {
  pinMode(RLed, OUTPUT);
  pinMode(GLed, OUTPUT);
  pinMode(YLed, OUTPUT);
}

void loop() {
  LedOn(RLed);
  LedOn(GLed);
  LedOn(YLed);

  delay(1000);
  LedOff(RLed);

  delay(1000);
  LedOff(GLed);

  delay(1000);
  LedOff(YLed);

  delay(1000);
}

void LedOn(int led){
  digitalWrite(led, HIGH);
}

void LedOff(int led){
  digitalWrite(led, LOW);
}
