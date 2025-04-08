// Define the analog pin connected to the potentiometer
const int potPin = A0;

// Define the digital pins connected to the push buttons
const int button1Pin = 2;
const int button2Pin = 3;
const int button3Pin = 4;

void setup() {
  // Start the Serial Monitor
  Serial.begin(9600);

  // Set the button pins as input (assuming external pull-down resistors)
  pinMode(button1Pin, INPUT);
  pinMode(button2Pin, INPUT);
  pinMode(button3Pin, INPUT);
}

void loop() {
  // Read the analog value from the potentiometer
  int potValue = analogRead(potPin);

  // Print the potentiometer value to the Serial Monitor
  Serial.println(potValue);

  // Check the state of each button (HIGH when pressed)
  if (digitalRead(button1Pin) == HIGH) {
    Serial.println("Button 1: 1");
  }

  if (digitalRead(button2Pin) == HIGH) {
    Serial.println("Button 2: 1");
  }

  if (digitalRead(button3Pin) == HIGH) {
    Serial.println("Button 3: 1");
  }

  // Add a small delay to make the output more readable
  delay(100);
}
