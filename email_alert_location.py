import time
import serial
import string
import pynmea2
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#setting up mail information
fromaddr = "sumitraspberry@gmail.com"
pword = "raspberry8008"
toaddr = "8008crce@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Location change alert"

#setup the serial port to which GPS is connected to
port = "/dev/ttyS0"
ser = serial.Serial(port, baudrate=9600, timeout=0.5)
dataout  = pynmea2.NMEAStreamReader()

while True:
    newdata = ser.readline()
    #print ("getting new lat")
    if newdata[0:6] == '$GPGGA':
        newmsg = pynmea2.parse(newdata)
        newlat = newmsg.latitude
        print(newlat)
        newlong = newmsg.longitude
        print(newlong)
        lat  = str(newlat)
        lon = str(newlong)
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

        time.sleep(10)
