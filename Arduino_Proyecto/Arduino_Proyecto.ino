// Pines de salida asociados a los índices
const int switches[3] = {4, 5, 7};

// Estado actual de los switches
bool switchStates[3] = {false, false, false};

// Tiempo para manejar tareas
unsigned long lastInputTime = 0;
unsigned long lastLightCheck = 0;

// Intervalos
const unsigned long inputInterval = 1000;     // 1 segundo
const unsigned long lightInterval = 30000;    // 15 segundos

void setup() {
  Serial.begin(9600);

  // Configurar pines como salida
  for (int i = 0; i < 3; i++) {
    pinMode(switches[i], OUTPUT);
    digitalWrite(switches[i], LOW);
  }
}

void loop() {
  unsigned long currentTime = millis();

  // Verifica input cada 1 segundo
  if (currentTime - lastInputTime >= inputInterval) {
    lastInputTime = currentTime;

    if (Serial.available()) {
      char input = Serial.read();

      // Controlar switches con '1', '2', '3'
      if (input >= '1' && input <= '3') {
        int index = input - '1';  // '1' -> 0, '2' -> 1, etc.
        switchStates[index] = !switchStates[index];  // Toggle
        digitalWrite(switches[index], switchStates[index] ? HIGH : LOW);
      }
    }
  }

  // Cada minuto: medir luz ambiente
  if (currentTime - lastLightCheck >= lightInterval) {
    lastLightCheck = currentTime;

    long sum = 0;
    for (int i = 0; i < 30; i++) {
      sum += analogRead(A0);
      delay(10);  // 10 ms entre lecturas
    }

    int average = sum / 30;
    Serial.print("IntL: ");
    Serial.println(average);
  }
}
