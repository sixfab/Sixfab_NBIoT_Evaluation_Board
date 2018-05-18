##getting started with SIXFAB NB-IoT EVB Shield
##pin Configuration 
##EVB   RPI
##5V -> 5V
##GND-> 5V
##RX -> GPIO15(RX)
##TX -> GPIO14(TX)

import time
import serial

###################################### 
#Change ip and port with your owns
ip  = "XX.XX.XX.XX"
port = "XXXX"
###################################### 

ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
)

print "Starting"
while 1:

        ser.reset_input_buffer()

        while 1:
                ser.write("AT+NRB\r")
                time.sleep(1)
                response = ser.readline()
                response = ser.readline()
                print 'RESPONSE:%s' % response

                if response.startswith('OK'):
                        break

        ser.reset_input_buffer()
        while 1:
                ser.write("AT+CGATT?\r")
                time.sleep(1)

                while 1:        

                        ser.write("AT+CGATT=1\r")
                        time.sleep(1)
                        ser.reset_input_buffer()
                        ser.write("AT+CGATT?\r")
                        time.sleep(1)
                        response = ser.readline()
                        response = ser.readline()
                        print 'RESPONSE:%s' % response

                        if response.startswith('+CGATT:1'):
                                break

                break

        ser.write('AT+NSOCL=0\r')
        time.sleep(1)


        ser.reset_input_buffer()

        while 1:
                ser.write("AT+NSOCR=DGRAM,17,3005,1\r")
                time.sleep(0.5)

                while 1:
                        response = ser.readline()
                        response = ser.readline()
                        print 'RESPONSE:%s' % response


                        if response.startswith('OK'):
                                break

                        if response.startswith('ERROR'):
                                ser.write("AT+NSOCR=DGRAM,17,3005,1\r")

                break

        break


while 1:

        while 1:

                print 'NUESTATS CHECKING'
                ser.reset_input_buffer()
                signal = 0
                while 1:
                        ser.write("AT+NUESTATS\r")
                        time.sleep(3)

                        while 1:
                                response = ser.readline()
                                print 'RESPONSE:%s' % response

                                if response.startswith('Signal power:'):
                                        signal = int(response.split(':',2)[1])/10

                                if response.startswith('OK'):
                                        break

                                time.sleep(0.1)

                        break

                data = 'Sixfab NB-IoT EVB\n'
		print data
                print 'SENDING DATA'
                data ="AT+NSOST=0," + ip + "," + port + ",{0},{1}\r".format(str(len(data)),data.encode("hex"))
                ser.reset_input_buffer()

                ser.write(data)

                response = ser.readline()
                response = ser.readline()
                print 'RESPONSE:%s' % response

                time.sleep(5)

                print 'FULL OK'










