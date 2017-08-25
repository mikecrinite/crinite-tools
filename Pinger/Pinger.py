"""
A script which will repeatedly ping a host and send an email to a given address regarding its status

Written by Michael Crinite while he should have been doing something productive instead

08.24.2017
"""

import logging
import os
import platform
import smtplib
import time
from datetime import *
from email import mime
from email.mime import multipart
from email.mime.text import MIMEText

from Pinger.credentials import get_creds

logger = logging.getLogger('Pinger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='Pinger.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
logger.addHandler(handler)

hostname = get_creds('hostname')
username = get_creds('username')
password = get_creds('password')
fromaddr = get_creds('fromaddr')
toaddr = get_creds('toaddr')  # For att users, you can text by sending an email to <phone-number>@att.txt.net

plat = platform.system().lower()
# TODO: keep all logs. Rename old logs and move them into the "logs" folder

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
    """
    Reports that the host is responding to a ping test

    Only sends update (pun intended) at the top of the hour
    """
    msg = "       " + hostname + " is online at: " + str(datetime.now())
    logger.info(msg)
    if datetime.now().minute % 60 == 0:
        send("Server online", msg)
        logger.info("Status message sent to: " + toaddr)


def offline():
    """ Reports that the host is not responding to a ping test """
    msg = "(!) " + hostname + " is OFFLINE at: " + str(datetime.now())
    send("Server OFFLINE", msg)
    logger.error(msg)
    logger.error("Status message sent to: " + toaddr)


while True:
    """ Tries a ping test to the server. Reports whether it was successful or not """
    if pingserv():
        online()
    else:
        offline()
    time.sleep(60)  # Wait for 10 minutes
