import time
import serial
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

TRIG = 19
ECHO = 26

gpio.setup(TRIG,gpio.OUT)
gpio.output(TRIG,gpio.LOW)
gpio.setup(ECHO,gpio.IN)
time.sleep(0.1)

print "====Start Measurement===="

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

distance = (stop-start)*340/2

print "%.3f" %distance

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

                data = '{{"_0":{0}, }}'.format(distance)
                print data
                print 'SENDING DATA'
                data ='AT+NSOST=0,78.183.178.242,5000,{0},{1}\r'.format(str(len(data)),data.encode("hex"))
                ser.reset_input_buffer()

                ser.write(data)


                response = ser.readline()
                response = ser.readline()
                print 'RESPONSE:%s' % response

                time.sleep(5)

                print 'OK'

