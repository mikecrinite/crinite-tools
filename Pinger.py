"""
A script which will repeatedly ping a server and report back if the server is offline

Written by Michael Crinite while he should have been doing something productive instead

***CURRENTLY A WORK IN PROGRESS!***

05.10.2016
"""

from datetime import *
import time
import smtplib
from email import mime
from email.mime import multipart
from email.mime.text import MIMEText
from credentials import get_creds
import logging
import os
import platform

logger = logging.getLogger('Pinger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='Pinger.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
logger.addHandler(handler)

# Name of server/website/computer name to ping
hostname = get_creds('hostname')
# Username for email account to log into
username = get_creds('username')
# Password for email account to log into
password = get_creds('password')
# Address to send mail from
fromaddr = get_creds('fromaddr')
# Address to send mail to (@att.txt.net)
toaddr = get_creds('toaddr')

plat = platform.system().lower()


def pingserv():
    """
    Pings the server
    Returns True if the server is online, False if the server is offline
    """
    ping_format = "-n" if plat == "windows" else "-c"
    ping = os.system("ping " + ping_format + " 1 " + hostname)
    logger.info("Pinged " + hostname)
    return ping == 0


def send(subject, body):
    """ Sends text message with report to toaddrs """
    # Format message
    msg = mime.multipart.MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(mime.text.MIMEText(body, 'plain'))
    message = msg.as_string()

    # Send message
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddr, message)
    server.quit()


def online():
    """ Reports twice per hour that the server is responding to a ping test """
    #if datetime.now().minute % 30 == 0:
    msg = "    " + hostname + " is online at: " + str(datetime.now())
    logger.info(msg)
    send("Server online", msg)


def offline():
    """ Reports once per minute whether or not the server is responding to a ping test """
    #if datetime.now().second % 60 == 0:
    msg = "(!) " + hostname + " is OFFLINE at: " + str(datetime.now())
    logger.error(msg)
    send("Server OFFLINE", msg)


while True:
    """ Tries a ping test to the server. Reports whether it was successful or not """
    if pingserv():
        online()
        time.sleep(300)
    else:
        offline()
        time.sleep(30)
