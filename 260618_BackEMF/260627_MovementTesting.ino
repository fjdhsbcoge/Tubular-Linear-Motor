#include <SimpleFOC.h>

// User's soldered pin configuration
#define PWM_A  6
#define PWM_B  10
#define PWM_C  5
#define EN     8

// DRV8313 fault/reset on Shield V3.2
#define DRV_RESET  A1
#define DRV_FAULT  A3

BLDCDriver3PWM driver = BLDCDriver3PWM(PWM_A, PWM_B, PWM_C, EN);
BLDCMotor motor = BLDCMotor(1);

const float POLE_PITCH_MM = 30.0;
const float MM_TO_RAD = 2.0f * PI / POLE_PITCH_MM;

float voltage_limit = 3.0;
float max_speed = 50.0;

enum MotorMode { MODE_STOP, MODE_VELOCITY, MODE_DISTANCE };
MotorMode currentMode = MODE_STOP;

float distance_velocity = 0;
unsigned long distance_start_ms = 0;
unsigned long distance_duration_ms = 0;

String inputBuffer = "";
unsigned long lastCharTime = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial);
  delay(100);

  Serial.println("\n=== SimpleFOC Shield V3.2 ===");
  Serial.println("Pins: A=6, B=10, C=5, EN=8");
  Serial.println("Timer note: pins 6 and 5 share Timer0 on Arduino Uno.");
  Serial.println("This is normal but may cause slight timing jitter.\n");

  // --- DRV8313 Reset sequence (CRITICAL) ---
  // The DRV8313 can latch into a fault state and needs a reset pulse
  pinMode(DRV_RESET, OUTPUT);
  digitalWrite(DRV_RESET, HIGH);
  delay(1);
  digitalWrite(DRV_RESET, LOW);
  delay(10);
  digitalWrite(DRV_RESET, HIGH);
  Serial.println("DRV8313 reset done");

  // Check fault status
  pinMode(DRV_FAULT, INPUT);
  delay(1);
  int fault = digitalRead(DRV_FAULT);
  Serial.print("DRV_FAULT (A3) = ");
  Serial.print(fault);
  Serial.println(fault == HIGH ? " (OK)" : " (FAULT!)");

  // --- 3PWM driver init ---
  driver.voltage_power_supply = 12;
  driver.voltage_limit = voltage_limit;
  driver.init();

  motor.linkDriver(&driver);
  motor.controller = MotionControlType::velocity_openloop;
  motor.voltage_limit = voltage_limit;
  motor.init();

  Serial.println("Driver init done");
  Serial.println("Commands: H, M50, D100, S, V50, L3.0, F, R");
  Serial.print(">>> ");
}

void loop() {
  // Serial reading with timeout flush
  while (Serial.available()) {
    char c = Serial.read();
    lastCharTime = millis();
    if (c == '\n' || c == '\r') {
      if (inputBuffer.length() > 0) { processCommand(inputBuffer); inputBuffer = ""; }
    } else {
      inputBuffer += c;
    }
  }
  if (inputBuffer.length() > 0 && (millis() - lastCharTime > 50)) {
    processCommand(inputBuffer); inputBuffer = "";
  }

  // Motor control
  switch (currentMode) {
    case MODE_VELOCITY:
      motor.move(distance_velocity * MM_TO_RAD);
      break;
    case MODE_DISTANCE:
      if (millis() - distance_start_ms < distance_duration_ms) {
        motor.move(distance_velocity * MM_TO_RAD);
      } else {
        motor.move(0);
        currentMode = MODE_STOP;
        Serial.println("OK: done");
        Serial.print(">>> ");
      }
      break;
    case MODE_STOP:
    default:
      motor.move(0);
      break;
  }
}

void processCommand(String cmd) {
  cmd.trim();
  if (cmd.length() == 0) return;

  Serial.print("Received: '");
  Serial.print(cmd);
  Serial.println("'");

  char c = cmd.charAt(0);
  String rest = cmd.substring(1);
  rest.trim();
  float value = rest.toFloat();

  switch (c) {
    case 'M': case 'm':
      if (abs(value) < 0.1) { stopMotor(); }
      else {
        currentMode = MODE_VELOCITY;
        distance_velocity = value;
        Serial.print("Velocity: ");
        Serial.print(value);
        Serial.println(" mm/s");
      }
      break;

    case 'D': case 'd':
      if (abs(value) < 0.1) { stopMotor(); }
      else if (max_speed < 0.1) { Serial.println("ERR: set V first"); }
      else {
        currentMode = MODE_DISTANCE;
        distance_velocity = (value > 0) ? max_speed : -max_speed;
        distance_duration_ms = (unsigned long)(abs(value) / max_speed * 1000.0);
        distance_start_ms = millis();
        Serial.print("Distance: ");
        Serial.print(value);
        Serial.print(" mm at ");
        Serial.print(max_speed);
        Serial.print(" mm/s for ");
        Serial.print(distance_duration_ms);
        Serial.println(" ms");
      }
      break;

    case 'S': case 's':
      stopMotor();
      break;

    case 'V': case 'v':
      max_speed = abs(value);
      Serial.print("Max speed: ");
      Serial.print(max_speed);
      Serial.println(" mm/s");
      break;

    case 'L': case 'l':
      voltage_limit = abs(value);
      driver.voltage_limit = voltage_limit;
      motor.voltage_limit = voltage_limit;
      Serial.print("Voltage limit: ");
      Serial.print(voltage_limit);
      Serial.println(" V");
      break;

    case 'F': case 'f':
      {
        int f = digitalRead(DRV_FAULT);
        Serial.print("Fault status: ");
        Serial.println(f == HIGH ? "OK" : "FAULT ACTIVE");
      }
      break;

    case 'R': case 'r':
      digitalWrite(DRV_RESET, LOW);
      delay(5);
      digitalWrite(DRV_RESET, HIGH);
      Serial.println("DRV8313 reset done");
      break;

    case 'H': case 'h': case '?':
      printHelp();
      break;

    default:
      Serial.println("ERR: unknown command. Type H for help.");
      break;
  }
  Serial.print(">>> ");
}

void stopMotor() {
  currentMode = MODE_STOP;
  motor.move(0);
  Serial.println("STOP");
}

void printHelp() {
  Serial.println("--- Commands ---");
  Serial.println("M50   Move at 50 mm/s");
  Serial.println("D100  Move 100 mm");
  Serial.println("S     Stop");
  Serial.println("V50   Set max speed");
  Serial.println("L3.0  Set voltage limit");
  Serial.println("F     Check DRV8313 fault status");
  Serial.println("R     Reset DRV8313");
  Serial.println("H     Help");
  Serial.println("--- Shield info ---");
  Serial.println("DRV8313 uses 3PWM + single enable");
  Serial.println("Your pins: A=6, B=10, C=5, EN=8");
  Serial.println("Reset (A1) and Fault (A3) are auto-checked at startup");
}
