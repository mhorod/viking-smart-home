#include <ArduinoHttpClient.h>
#include <WiFiNINA.h>
#include <ArduinoJson.h>
#include <Servo.h>

char ssid[] = "KPT-Conference";
char pass[] = "E2ue6Tm&";
char serverAddress[] = "172.98.2.114"; // server address
char endpoint[] = "/v1/drive";

WiFiClient wifi;
HttpClient client = HttpClient(wifi, serverAddress);
int status = WL_IDLE_STATUS;

// Left Motor (A)
int COHON0_DRIVE_POWER_DEVICE = A0;
// Right Motor (B)
int COHON1_DRIVE_POWER_DEVICE = A7;

int SWORD_COHONES_POWER_DEVICE = A3;

int TRIG_DISTANCE = A1;
int ECHO_DISTANCE = A2;

int SPEED = 255;

Servo cochon0;
Servo cochon1;
Servo cochonesMegaGrandes;

int pin = 12;

int big_flippa = 0;
int cohone = 0;

void setup() {
  Serial.begin(9600);
  // while (!Serial);

  pinMode(pin, OUTPUT);
  digitalWrite(pin, HIGH);

  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid); // print the network name (SSID);

    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);
  }

  digitalWrite(pin, LOW);

  Serial.println("Connected!");


  cochon0.attach(COHON0_DRIVE_POWER_DEVICE); // attach the servo to our servo object
  cochon0.write(90); // stop the motor

  cochon1.attach(COHON1_DRIVE_POWER_DEVICE);
  cochon1.write(90);

  cochonesMegaGrandes.attach(SWORD_COHONES_POWER_DEVICE);
  cochonesMegaGrandes.write(90);

  pinMode(TRIG_DISTANCE, OUTPUT); //Pin, do którego podłączymy trig jako wyjście
  pinMode(ECHO_DISTANCE, INPUT);

  // enable ports
  // pinMode(enA, OUTPUT);
  // pinMode(enB, OUTPUT);
  // pinMode(in1, OUTPUT);
  // pinMode(in2, OUTPUT);
  // pinMode(in3, OUTPUT);
  // pinMode(in4, OUTPUT);
}

void cochonesGrandes(int speedA, int speedB) {
  // if (speedA == 0) {
  //   digitalWrite(in1, LOW);
  //   digitalWrite(in2, LOW);
  // } else if (speedA > 0) {
  //   digitalWrite(in1, HIGH);
  //   digitalWrite(in2, LOW);
  // } else {
  //   digitalWrite(in1, LOW);
  //   digitalWrite(in2, HIGH);
  // }

  // if (speedB == 0) {
  //   digitalWrite(in3, LOW);
  //   digitalWrite(in4, LOW);
  // } else if (speedB > 0) {
  //   digitalWrite(in3, HIGH);
  //   digitalWrite(in4, LOW);
  // } else {
  //   digitalWrite(in3, LOW);
  //   digitalWrite(in4, HIGH);
  // }

  analogWrite(COHON0_DRIVE_POWER_DEVICE, abs(speedA));
  analogWrite(COHON1_DRIVE_POWER_DEVICE, abs(speedB));
}
	
int zmierzOdleglosc() {
  long czas, dystans;
 
  digitalWrite(TRIG_DISTANCE, HIGH);
  delayMicroseconds(2);
  digitalWrite(TRIG_DISTANCE, LOW);
  delayMicroseconds(10);
  digitalWrite(TRIG_DISTANCE, HIGH);
 
  czas = pulseIn(ECHO_DISTANCE, !HIGH);
  dystans = czas / 58;
 
  return dystans;
}

void loop() {
  Serial.print("Sending GET request to ");
  Serial.println(endpoint);
  client.get(endpoint);

  JsonDocument doc;

  int statusCode = client.responseStatusCode();
  String response = client.responseBody();

  deserializeJson(doc, response);

  int x = 0, y = 0, speedA = 0, speedB = 0;

  Serial.print("Status code: ");
  Serial.println(statusCode);

  Serial.print("X: ");
  x = (int)doc["x"];
  x = x == 2 ? -1 : x;
  Serial.println(x);

  Serial.print("Y: ");
  y = (int)doc["y"];
  y = y == 2 ? -1 : y;
  Serial.println(y);

  int temp = x;
  x = -y;
  y = temp;

  if (x != 0 && y == 0) {
    speedA = x * SPEED;
    speedB = speedA; 
  }

  else if (y != 0 && x == 0) {
    speedA = y * SPEED;
    speedB = -speedA;
  }

  else {
    if (x == 1 && y == 1) {
      speedA = SPEED;
      speedB = -SPEED/2;
    } else if (x == 1 && y == -1) {
      speedA = -SPEED/2;
      speedB = SPEED;
    } else if (x == -1 && y == 1) {
      speedA = -SPEED;
      speedB = SPEED/2;
    } else if (x == -1 && y == -1) {
      speedA = SPEED/2;
      speedB = -SPEED;
    }
  }

  // Serial.print(speedA);
  // cochonesGrandes(speedA, speedB);



  // cochon0.write(45);
  cochon0.write(speedA == 0 ? 90 : (speedA > 0 ? 45 : 135));
  cochon1.write(speedB == 0 ? 90 : (speedB > 0 ? 45 : 135));

  if (big_flippa) {
    cochonesMegaGrandes.write(45);
  }
  else {
    cochonesMegaGrandes.write(135);
  }

  big_flippa = !big_flippa;

  // cohone++;
  // if (cohone == 9) {
  //   Serial.println(zmierzOdleglosc());
  //   cohone = 0;
  // }
  
  // for (int i = 0; i < 180; i++) {
  //     cochon0.write(i);
  //     cochon1.write(i);
  //     Serial.println(i);
  //     delay(100);
  // }

  delay(100);
}
