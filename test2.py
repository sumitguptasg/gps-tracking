import time
import serial
import string
import pynmea2
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from math import sin, cos, sqrt, atan2, radians
#setting up mail information
fromaddr = "sumitraspberry@gmail.com"
pword = "raspberry8008"
toaddr = "8008crce@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Location change alert"
flag=0
lat0=0
lon0=0
lat=0
lon=0
def calculate(lt1,ln1,lt2,ln2):
	# approximate radius of earth in km
	R = 6373.0

	lat1 = radians(lt1)
	lon1 = radians(ln1)
	lat2 = radians(lt2)
	lon2 = radians(ln2)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
        return distance


#setup the serial port to which GPS is connected to
port = "/dev/ttyS0"
ser = serial.Serial(port, baudrate=9600, timeout=0.5)
dataout  = pynmea2.NMEAStreamReader()
while True:
    newdata = ser.readline()
   # print ("getting new location")
    if newdata[0:6] == '$GPGGA':
        newmsg = pynmea2.parse(newdata)
        newlat = newmsg.latitude
        print(newlat)
        newlong = newmsg.longitude
        print(newlong)
        lat  = str(newlat)
        lon = str(newlong)
	if(flag==0):
		lat0=lat
		lon0=lon
		flag=1

    if (calculate(float(lat0),float(lon0),float(lat),float(lon))>=0):

        content = "http://maps.google.com/maps?q=" + lat + "," + lon

        Email = content
        msg.attach(MIMEText(Email, 'plain'))
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, pword)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            print ("mail sent!")
        except:
            print("error, couldnt send mail, be sure to enable non secure apps login on sender's email")
    lat0=lat
    lon0=lon
    time.sleep(2)
