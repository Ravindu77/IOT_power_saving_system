String s; // for incoming serial data

const int RLed = 3;

void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  pinMode(RLed, OUTPUT);
}

void loop() {
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    s = Serial.readString();

    // say what you got:
    Serial.print("I received: ");
    Serial.println(s);

    if(s == "Hello"){
      LedOn(RLed);
    }
  }
}

void LedOn(int led){
  digitalWrite(led, HIGH);
}

void LedOff(int led){
  digitalWrite(led, LOW);
}
