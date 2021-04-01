int redButtonState = 0;
int blueButtonState = 0;
int switchState = 0;
int x = 0;
int y = 0;
String vals;

void setup() {
 Serial.begin(115200);
 pinMode(16, OUTPUT); // Red LED
 pinMode(17, OUTPUT); // Blue LED
 pinMode(5, INPUT); // Red Button
 pinMode(18, INPUT); // Blue Button
 pinMode(19, INPUT); // Switch
}

void loop() {
  switchState = digitalRead(19);
  if (switchState == 1) {
    digitalWrite(16, LOW);
    digitalWrite(17, HIGH);
    
    x = analogRead(34);
    y = analogRead(35);
    
    redButtonState = digitalRead(5);
    blueButtonState = digitalRead(18);
    String vals = String(x) + ',' + String(y) + ',' + String(redButtonState) + ',' + String(blueButtonState);
    Serial.println(vals);
  } else {
    digitalWrite(16, HIGH);
    digitalWrite(17, LOW);
  }
  delay(100);
}
