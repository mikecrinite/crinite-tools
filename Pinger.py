# # #
# A script which will repeatedly ping a server and report back if the server is offline
#
# Written by Michael Crinite while he should have been doing something productive instead
#
# ***CURRENTLY A WORK IN PROGRESS!***
#
# 05.10.2016
# # #

from datetime import *
import time
import smtplib
from email import mime
from email.mime import multipart
from email.mime.text import MIMEText

# Name of server/website/computer name to ping
hostname = input("Enter IP address of server: \n")
# Username for email account to log into
username = input("Enter username: ")
# Password for email account to log into
password = input("Enter password: ");
# Address to send mail from
fromaddr = input("Enter address to send from: ")
# Address to send mail to (@att.txt.net)
toaddrs = input("Enter address to send to: ")


# Pings the server
# Returns True if the server is online, False if the server is offline
def pingserv():
    # Determine what OS the program is running on
    import os, platform, subprocess
    plat = platform.system().lower()
    ping_format = ""
    if plat == "windows":
        ping_format = "-n"
    else:
        ping_format = "-c"

    # ping = os.system("ping " + ping_format + " 1 " + hostname)
    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(['ping', ping_format, '1', hostname], stdout=DEVNULL, stderr=DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False


# Sends text message with report to toaddrs
def send(subject, body):
    # Format message
    msg = mime.multipart.MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    msg['Subject'] = subject
    msg.attach(mime.text.MIMEText(body, 'plain'))
    message = msg.as_string()

    # Send message
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(FROM, TO, message)
    server.quit()


# Reports twice per hour that the server is responding to a ping test
def online():
    if datetime.now().minute % 30 == 0:
        subject = "Server online"
        msg = "    " + hostname + " is online at: " + str(datetime.now())
        print(msg)
        send(subject, msg)
        time.sleep(300)
    return True


# Reports once per minute that the server is responding to a ping test so that
# You don't have to wait a half hour for the response via online()
def onlinedebugmode():
    if datetime.now().second & 60 == 0:
        subject = "Server online"
        msg = "    " + hostname + " is online at: " + str(datetime.now())
        print(msg)
        send(subject, msg)
        time.sleep(30)
    return True


# Reports once per minute that the server is not responding to a ping test
def offline():
    if datetime.now().second % 60 == 0:
        subject = "Server OFFLINE"
        msg = "(!) " + hostname + " is OFFLINE at: " + str(datetime.now())
        # print("(!)", hostname, "is OFFLINE at: ", datetime.now())
        print(msg)
        send(subject, msg)
        time.sleep(30)
    return True


# Tries a ping test to the server. Reports whether it was successful or not
while True:
    if pingserv():
        online()
        # onlinedebugmode()
    else:
        offline()
