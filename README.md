# NB-IoT-EVB
This is the repository of [sixfab nb-iot evaluation board](https://sixfab.com/product/nb-iot-evaluation-board/).

# Available Libraries
### using with arduino
Checkout https://github.com/sixfab/Sixfab_Arduino_NBIoT_Library
Library Defined Arduino Pins:
```
#define USER_BUTTON 8
#define USER_LED 6
#define BC95_ENABLE 4
#define ALS_PT19_PIN A1
#define RELAY 5

#define BC95_AT Serial // BC95 AT Command Serial at 115200 baudrate
SoftwareSerial DEBUG(10,11); // RX, TX - DEBUG PORT at 9600 baud rate (use with TTL2USB Converter)
```

### using with raspberry pi
Checkout https://github.com/sixfab/Sixfab_RPi_NBIoT_Library
Library Defined Pins:
```
USER_BUTTON = 21
USER_LED = 20
RESET = 16
RELAY = 26
OPTO1 = 12
OPTO2 = 5
VDD_EXT = 6
LUX_CHANNEL = 0

serial_port="/dev/ttyS0" at 9600 baudrate (if you use any older version than RPi 3, serial_port must be '/dev/ttyAMA0')
```


# Examples
### using with arduino
** [localHost](https://github.com/sixfab/Sixfab_Arduino_NBIoT_Library/blob/master/examples/localHost/localHost.ino)

### using with raspberry pi 
** [basicUDP](https://github.com/sixfab/Sixfab_RPi_NBIoT_Library/blob/master/sample/basicUDP.py)  
** [sensorTest](https://github.com/sixfab/Sixfab_RPi_NBIoT_Library/blob/master/sample/sensor_test.py)

# Tutorials will be here very soon

# Pinout
<img src="https://sixfab.com/wp-content/uploads/2018/10/nbiot_eval_board_pinout.png" width="480">

# Attention
! All data pins work with 3.3V reference. Any other voltage level should harm your device.

# Layout
![Layout](https://sixfab.com/wp-content/uploads/2018/10/nbiot_evaluation_board_layout-1.png)
