##This code tests SIXFAB NB-IoT EVB Shield
##pin Configuration 
##EVB   	RPI
##5V 	-> 	5V
##GND	-> 	5V
##RX 	-> 	GPIO15(RX)
##TX 	-> 	GPIO14(TX)
##
##JSN-SR04	RPi
##5V	->	5V
##GND	->	GND
##TRIG	->	GPIO19
##ECHO	->	GPIO26

import time
import serial
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

###################################### 
#Change ip and port with your owns
ip  = "XX.XX.XX.XX"
port = "XXXX"
###################################### 

TRIG = 19
ECHO = 26


gpio.setup(TRIG,gpio.OUT)
gpio.output(TRIG,gpio.LOW)
gpio.setup(ECHO,gpio.IN)
time.sleep(0.1)

def cal_distance():
	gpio.output(TRIG,gpio.HIGH)
	time.sleep(0.00001) #Trigger high for 0.1us
	gpio.output(TRIG,gpio.LOW)

	##two times are recorded at the beginning and at the end of the pulse

	## the while loop will begin to continue until the input becomes high
	## then the time is marked
	while gpio.input(ECHO) == 0:
        	pass

	start = time.time() #expresses the current time in seconds

	while gpio.input(ECHO) == 1:
        	pass

	stop = time.time()
	#print stop-start
	distance = (stop-start)*340*100/2	#returns in cm

	#print "%.3f" %distance
	if distance > 20 and distance < 600:
		return distance
	else:
		return 'OFF RANGE'
 

#########------------------------------------

ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
)


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

#        print 'DONE 1'

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

#        print 'DONE 2'

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

#        print 'DONE 3'
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
                while 1:
                	data = '{{Distance: {0}}}\n'.format(cal_distance())
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










