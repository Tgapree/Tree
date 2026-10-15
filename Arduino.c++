#include <DHT.h>

#define DHTPIN 3
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup()
{

    Serial.begin(9600);

    pinMode(A0, INPUT); // Soil sensor
    pinMode(2, INPUT);  // Light sensor

    dht.begin();
}

void loop()
{

    int soil = analogRead(A0);  // Soil moisture
    int light = digitalRead(2); // Light sensor

    float temp = dht.readTemperature();
    float humidity = dht.readHumidity();

    // ถ้า DHT อ่านไม่ได้
    if (isnan(temp) || isnan(humidity))
    {
        temp = 0;
        humidity = 0;
    }

    // ส่งข้อมูลให้ Raspberry Pi
    Serial.print(soil);
    Serial.print(",");
    Serial.print(light);
    Serial.print(",");
    Serial.print(temp);
    Serial.print(",");
    Serial.println(humidity);

    delay(2000); // อ่านทุก 2 วินาที
}