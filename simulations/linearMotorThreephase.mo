model lineasrmotor_elektrisch
  Modelica.Electrical.Analog.Basic.Ground ground annotation(
    Placement(transformation(origin = {-76, -52}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Basic.Resistor resistor(R = 5.6)  annotation(
    Placement(transformation(origin = {-44, 48}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Basic.Inductor inductor(L(displayUnit = "mH") = 0.00115)  annotation(
    Placement(transformation(origin = {-8, 48}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Sources.SineVoltage sineVoltage(V = 4, phase = -2.6179938779914944, f = 1, startTime = 0.1)  annotation(
    Placement(transformation(origin = {-76, 48}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Sensors.CurrentSensor currentSensor annotation(
    Placement(transformation(origin = {42, 48}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Basic.Resistor resistor1(R = 5.6) annotation(
    Placement(transformation(origin = {-42, 22}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Basic.Inductor inductor1(L(displayUnit = "mH") = 0.00115) annotation(
    Placement(transformation(origin = {-6, 22}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Sources.SineVoltage sineVoltage1(V = -4*0, f = 1, phase = 2.6179938779914944, startTime = 0.1) annotation(
    Placement(transformation(origin = {-74, 22}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Sensors.CurrentSensor currentSensor1 annotation(
    Placement(transformation(origin = {44, 22}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Basic.Resistor resistor2(R = 5.6) annotation(
    Placement(transformation(origin = {-42, -4}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Basic.Inductor inductor2(L(displayUnit = "mH") = 0.00115) annotation(
    Placement(transformation(origin = {-6, -4}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Sources.SineVoltage sineVoltage2(V = 4, f = 1, phase = 1.5707963267948966, startTime = 0.1) annotation(
    Placement(transformation(origin = {-74, -4}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Sensors.CurrentSensor currentSensor2 annotation(
    Placement(transformation(origin = {44, -4}, extent = {{-10, -10}, {10, 10}})));

  model LinearMotor_MathOnly
    parameter Real R = 5.6;
    parameter Real L = 0.00115;
    parameter Real M = -0.00046;
    parameter Real V_peak = 8.0;
    parameter Real f = 50;
    
    Real i_a, i_b, i_c;         // 3 Ströme
    Real v_La, v_Lb, v_Lc;        // 3 Induktivitätsspannungen
    Real v_n;                   // 1 Sternpunktspannung (floating neutral)
    // Total: 7 Variablen
    
  initial equation
    i_a = 0; 
    i_b = 0; 
    i_c = 0;
  
  equation
    // 3 Spannungsgleichungen (Kirchhoff Voltage Law)
    // V_source - v_n = R*i + v_L
    V_peak * sin(2*Modelica.Constants.pi*f*time - 2.618) - v_n = R*i_a + v_La;
    -V_peak * sin(2*Modelica.Constants.pi*f*time + 2.618) - v_n = R*i_b + v_Lb;  
    V_peak * sin(2*Modelica.Constants.pi*f*time + 1.571) - v_n = R*i_c + v_Lc;
    
    // 3 Kopplungsgleichungen (mutual inductance)
    v_La = L*der(i_a) + M*der(i_b) + M*der(i_c);
    v_Lb = M*der(i_a) + L*der(i_b) + M*der(i_c);
    v_Lc = M*der(i_a) + M*der(i_b) + L*der(i_c);
    
    // 1 Kirchhoff Current Law (Summe der Ströme = 0)
    i_a + i_b + i_c = 0;
    
    // Total: 7 Gleichungen für 7 Variablen → System ist bestimmt!
  end LinearMotor_MathOnly;
equation
  connect(sineVoltage.p, ground.p) annotation(
    Line(points = {{-86, 48}, {-92, 48}, {-92, -42}, {-76, -42}}, color = {0, 0, 255}));
  connect(sineVoltage2.p, ground.p) annotation(
    Line(points = {{-84, -4}, {-90, -4}, {-90, -42}, {-76, -42}}, color = {0, 0, 255}));
  connect(sineVoltage1.p, ground.p) annotation(
    Line(points = {{-84, 22}, {-90, 22}, {-90, -42}, {-76, -42}}, color = {0, 0, 255}));
  connect(sineVoltage2.n, resistor2.p) annotation(
    Line(points = {{-64, -4}, {-52, -4}}, color = {0, 0, 255}));
  connect(sineVoltage1.n, resistor1.p) annotation(
    Line(points = {{-64, 22}, {-52, 22}}, color = {0, 0, 255}));
  connect(sineVoltage.n, resistor.p) annotation(
    Line(points = {{-66, 48}, {-54, 48}}, color = {0, 0, 255}));
  connect(resistor.n, inductor.p) annotation(
    Line(points = {{-34, 48}, {-18, 48}}, color = {0, 0, 255}));
  connect(inductor.n, currentSensor.p) annotation(
    Line(points = {{2, 48}, {32, 48}}, color = {0, 0, 255}));
  connect(currentSensor.n, currentSensor1.n) annotation(
    Line(points = {{52, 48}, {74, 48}, {74, 22}, {54, 22}}, color = {0, 0, 255}));
  connect(currentSensor2.n, currentSensor1.n) annotation(
    Line(points = {{54, -4}, {74, -4}, {74, 22}, {54, 22}}, color = {0, 0, 255}));
  connect(currentSensor1.p, inductor1.n) annotation(
    Line(points = {{34, 22}, {4, 22}}, color = {0, 0, 255}));
  connect(inductor1.p, resistor1.n) annotation(
    Line(points = {{-16, 22}, {-32, 22}}, color = {0, 0, 255}));
  connect(resistor2.n, inductor2.p) annotation(
    Line(points = {{-32, -4}, {-16, -4}}, color = {0, 0, 255}));
  connect(inductor2.n, currentSensor2.p) annotation(
    Line(points = {{4, -4}, {34, -4}}, color = {0, 0, 255}));
  annotation(
    uses(Modelica(version = "4.0.0")));
end lineasrmotor_elektrisch;
