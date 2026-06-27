#include <SimpleFOC.h>

// DRV8313 pins (from your Arduino sketch)
#define INA  9   // PWM pins!
#define INB  10
#define INC  11
#define ENA  7   // Enable pins
#define ENB  6
#define ENC  5

// 1 pole-pair = 1 pole-pitch = 30 mm
BLDCMotor motor = BLDCMotor(1);
BLDCDriver3PWM driver = BLDCDriver3PWM(INA, INB, INC, ENA, ENB, ENC);

// Conversion: 30 mm pole-pitch = 2π electrical radians
const float POLE_PITCH_MM = 30.0;
const float MM_TO_RAD = 2.0 * PI / POLE_PITCH_MM;  // 0.2094 rad/mm
const float R_PHASE = 4.8;   // Ohm
const float KT = 6.29;       // N/A (from your back-EMF)

void setup() {
  Serial.begin(115200);
  delay(1000);

  driver.voltage_power_supply = 12;  // Your supply voltage
  driver.voltage_limit = 3.0;        // START LOW! ~0.6A at stall
  driver.init();

  motor.linkDriver(&driver);
  motor.controller = MotionControlType::velocity_openloop;
  motor.voltage_limit = 3.0;         // Same as driver limit
  motor.init();

  Serial.println("Motor ready");
}

void loop() {
  // --- Test 1: Move at 50 mm/s for 2 seconds ---
  float target_mm_s = 50.0;
  float target_rad_s = target_mm_s * MM_TO_RAD;
  
  motor.move(target_rad_s);
  delay(2000);

  // --- Stop (velocity = 0) ---
  motor.move(0);
  delay(1000);
}