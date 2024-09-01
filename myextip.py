# -*- coding: utf-8 -*-
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import os
import datetime
import time
import re
import smtplib
import random

def requests_retry_session(
    retries=50,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session



while True:

    mainurl = 'https://checkip.amazonaws.com'
    
    server = smtplib.SMTP('IP', PORT)
    server.login("USERNAME", "PASSWORD")
    mainurl = requests_retry_session().get(mainurl)
    latestextip = BeautifulSoup(mainurl.text.encode('utf-8'), 'html.parser')

    headers = ("Message-ID: <"+str(random.randint(1000000000000000000000000000,9999999999999999999999999999))+"@mailer.DOMAIN.com>\nFrom: name1 <user1@domain1.com>\nTo: name2 <user2@domain2.com>\nSubject: New External IP Address\nMIME-Version: 1.0\nContent-Type: text/html; charset=utf-8\nContent-Transfer-Encoding: 8bit\n")

    latestextip = (latestextip).text
    print('Prettified: '+str(latestextip))
    f = open( 'PATHTOTEMPTXTFILE/latestip.txt', 'r' )
    if (not (latestextip in f.read())):
        msg = ('\n\n<!DOCTYPE html><head><meta charset="UTF-8"></head><body><p style="margin-top:0in;margin-right:0in;margin-bottom:8.0pt;margin-left:0in;line-height:107%;font-size:15px;font-family:&quot;Calibri&quot;,sans-serif;">New external IP address: '+latestextip.encode('utf-8')+'\n<br></p>'+'</body></html>\n\n')
        server.sendmail("MAILFROMADDRESS", "MAILTOADDRESS", headers+msg)
        f.close()
        f = open('PATHTOTEMPTXTFILE/latestip.txt', 'w')
        print ('Saved in the temp file: '+str(latestextip))
        f.seek(0,2)
        f.write(latestextip.encode('utf-8'))
        f.close()
    else: print('No new external IP address was detected. Nothing written in the temp file.\n')
    f.close()



    server.quit
    print('Cycle done! '+str(datetime.datetime.now())[0:-7]+'\n\n\n')
    for i in range(3600):
       time.sleep(1)
