#!/usr/bin/python
import logging
import signal
import sys
#from time import sleep
import RPi.GPIO as GPIO
import serial
import time
import smtplib
from email.mime.multipart import MIMEMultipart

serialport="/dev/ttyACM0"
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='thermosifon.log',level=logging.DEBUG)
# Set up the GPIO channels - one output
GPIO.setup(12, GPIO.OUT)
# Output to pin 12
def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        GPIO.output(12, False)
        logging.info('false')
	ser.close()             # close port
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

to  = '@net.gr'
me  = 'sms@gmail.com'
# Create the container (outer) email message.
msg = MIMEMultipart()
msgoff = MIMEMultipart()
#msg['Subject'] = 'O thermosifonas anoi3e!'
msg['From'] = me
msg['To'] = to
msg.preamble = 'To minima'
msgoff['From'] = me
msgoff['To'] = to
msgoff.preamble = 'To minima'

# Credentials (if needed)
username = 'sms'
password = 'pass'

# The actual mail send
#try:
#	server = smtplib.SMTP('smtp.gmail.com:587')
#except Exception:
#	print "Error: unable to connect to server!"
timeout = 10
offafter = 15*60
first_time = time.time()
last_time = first_time
number = "6980000000"
number2 = "6970000000"
number3 = "26100000000"
therm = 0
ser = serial.Serial(serialport, 9600)
print ser.portstr       # check which port was really used
at_command = 'AT+CLIP=1,1\r\n'
ser.write(at_command)
ser.sendBreak()
line = ser.read(ser.inWaiting())
print line
logging.info('To script 3ekina!')
while 1:
	line =  ser.readline()
	if line.find(number) > 0 or line.find(number2) > 0 or line.find(number3) > 0 :
		new_time = time.time()
#		print "O",number,"kalei"
		if  new_time - last_time > timeout:
		        last_time = new_time
		        print "Its been %f seconds" % (new_time - first_time)
			if therm == 0: 
				therm = 1
			        GPIO.output(12, True)
				logging.info('O thermosifonas anoi3e gia %d lepta',  (offafter/60))
				msg['Subject'] = "O thermosifonas anoi3e gia %d lepta" % (offafter/60)
				try:
					server = smtplib.SMTP('smtp.gmail.com:587')
					server.starttls()
					server.login(username,password)
					server.sendmail(me, to, msg.as_string())
					server.quit()
					print "Successfully sent sms"
					del server
				except Exception:
   					print "Error: unable to send email"
				time.sleep(offafter)
				GPIO.output(12, False)
				logging.info("O thermosifonas ekleise")
				therm = 0
				msgoff['Subject'] = "O thermosifonas ekleise"
				try:
					server = smtplib.SMTP('smtp.gmail.com:587')
					server.starttls()
					server.login(username,password)
					server.sendmail(me, to, msgoff.as_string())
					server.quit()
					logging.info("Successfully sent sms")
					del server
				except Exception:
   					print "Error: unable to send email"			
ser.close()             # close port

