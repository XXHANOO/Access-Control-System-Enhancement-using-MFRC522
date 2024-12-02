#include <SPI.h>
#include <MFRC522.h>

// Pin definitions
#define SS_PIN 10
#define RST_PIN 9
#define AM_TX_PIN 5 // Transmitter pin for FS1000A module

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  pinMode(AM_TX_PIN, OUTPUT);
  Serial.println("Access Control System Initialized. Place your card...");
}

void loop() {
  // Check if a new card is present
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // Read and print card UID
  Serial.print("Card UID: ");
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    Serial.print(" ");
  }
  Serial.println();

  // Simulate access control decision
  if (isAuthorized(mfrc522.uid.uidByte, mfrc522.uid.size)) {
    Serial.println("Access Granted!");
    sendSignalToAMModule(true); // Send authorized signal
  } else {
    Serial.println("Access Denied!");
    sendSignalToAMModule(false); // Send unauthorized signal
  }

  delay(1000); // Wait before reading again
}

// Check if card UID is authorized (example logic)
bool isAuthorized(byte *uid, byte uidSize) {
  byte authorizedUID[] = {0xDE, 0xAD, 0xBE, 0xEF}; // Example authorized UID
  if (uidSize != sizeof(authorizedUID)) return false;

  for (byte i = 0; i < uidSize; i++) {
    if (uid[i] != authorizedUID[i]) return false;
  }
  return true;
}

// Send signal to AM module
void sendSignalToAMModule(bool accessGranted) {
  if (accessGranted) {
    digitalWrite(AM_TX_PIN, HIGH);
    delay(200); // Simulate signal duration
    digitalWrite(AM_TX_PIN, LOW);
    Serial.println("AM Module: Authorized signal sent.");
  } else {
    digitalWrite(AM_TX_PIN, HIGH);
    delay(500); // Longer signal for unauthorized
    digitalWrite(AM_TX_PIN, LOW);
    Serial.println("AM Module: Unauthorized signal sent.");
  }
}
