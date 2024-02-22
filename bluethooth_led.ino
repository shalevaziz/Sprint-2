//We start by setting up some constants
#define LED_PIN 8
#define TURN_ON '1'
#define TURN_OFF '0'
void setup()
{
  Serial.begin(9600); //Begin serial communication
  pinMode(LED_PIN, OUTPUT); //We want to tell the arduino that we will output voltage to the LED_PIN
}
void loop()
{
  if(Serial.available()>0) //If we recived data
  {
    char data= Serial.read(); // Read one byte (char) from the bluetooth module
    if(data == TURN_ON) // If that one byte is the TURN_ON byte turn the led on
      {
      digitalWrite(LED_PIN, HIGH);
      }
    else if(data == TURN_OFF) //else if it is TURN_OFF turn the led off
    {
    digitalWrite(LED_PIN, LOW);
    }
    Serial.print(data); //Send back the data to the sender (This way we can
    see that we recived data)
  }
  delay(50);
}