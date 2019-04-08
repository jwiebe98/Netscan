#Import Libraries
import smtplib, ssl
from datetime import datetime

#Email credentials and port.
smtp_server = "smtp.gmail.com"
port = 587 #startttls
password = "" #Enter Email and Password for the gmail account
email = "" 

#Function used to email if a device is down
def email_down(dev, recipients):
        
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(email, password)   
        
        message = """
Device: {}
MAC: {}
IP: {}
Status: Down
Last Uptime: {}
            
Please check this device for correct operation.
""".format(dev.device, dev.mac, dev.ip, dev.first_ping)
        print("sending email")
        server.sendmail(email, recipients, message)
        server.close()

#Function used to email if a device is down
def email_up(dev, recipients):
        
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(email, password)   
        
        message = """
Device: {}
MAC: {}
IP: {}
Status: Up
Uptime: {}
            
This Device is back online.
""".format(dev.device, dev.mac, dev.ip, dev.first_ping)
        print("sending email")
        server.sendmail(email, recipients, message)
        server.close()
