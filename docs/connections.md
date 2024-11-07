# Connection Chart

Here we are using ***Aurdino Nano*** for this project

> [!NOTE]
> This is same for HADCs and LADCs
> Only thing is HADC Receiver not include sensors
---
| Component  | Pin on Module | Pin on Arduino Nano | Pins (A)  | To Pins | Done |
| ---------- | ------------- | ------------------- | --------- | ------- | ---- |
| MQ-135     | VCC           | 5V                  | _18F_     | -       | ✔    |
|            | GND           | GND                 | 12F       | -       | ✔    |
|            | AOUT          | A0                  | 18N       | -       | ✔    |
| DHT22      | VCC           | 5V                  | _18F_ | -       | ✔    |
|            | GND           | GND                 | 12F       | -       | ✔    |
|            | DATA          | D3                  | 12H       | -       | ✔    |
| LoRa RA-02 | VCC           | 3.3V                | _18F_     | 6F      | ✔    |
|            | GND           | GND                 | _12F_     | 8P      | ✔    |
|            | MISO          | D12                 | 12Q       | 5P      | ✔    |
|            | MOSI          | D11                 | 12P       | 6P      | ✔    |
|            | SCK           | D13                 | 18Q       | 4P      | ✔    |
|            | NSS           | D10                 | 12O       | 7P      | ✔    |
|            | RST           | D9                  | 12N       | 5F      | ✔    |
|            | DIO0          | D2                  | 12G       | 4F      | ✔    |

---
You can expand on our own