const int buttonPin = 2;
int buttonState = 0;

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT);
}

void loop() {
 
  button(buttonState);
}

//Function Button
bool button(int buttonState){
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) {
    Serial.print("On \n");
    delay(500);
    return true;
  } else{
    return false;
  }
}
