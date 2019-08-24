# Auto Send Mail

## 参考文档

* [RPi 2B 自动发送获取的IP到固定邮箱](https://www.cnblogs.com/zengjfgit/p/5205338.html)

## code

```python
#!/usr/bin/python3

import subprocess
import smtplib
from email.mime.text import MIMEText
import datetime
import time
import os

def check_ping():
    hostname = "www.baidu.com"
    response = os.system("ping -c 1 " + hostname)

    # and then check the response...
    if response == 0:
        pingstatus = True
    else:
        pingstatus = False

    return pingstatus

while True:
    if check_ping():
        break

    time.sleep(1)

# Change to your own account information
# Account Information
to            = 'zengjf42@163.com'           # Email to send to.
mail_user     = 'zengjf42@163.com'           # Email to send from.
mail_password = 'zjf199042zjf'               # Email password.
smtpserver    = smtplib.SMTP('smtp.163.com') # Server to use.

smtpserver.ehlo()                            # Says 'hello' to the server
smtpserver.starttls()                        # Start TLS encryption
smtpserver.ehlo()
smtpserver.login(mail_user, mail_password)   # Log in to server
today = datetime.date.today()                # Get current time/date

arg='ifconfig -a'                            # Linux command to retrieve ip addresses.
# Runs 'arg' in a 'hidden terminal'.
p=subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
data = p.communicate()                       # Get data from 'p terminal'.
# print(data)

# get ip data
ip_lines = data[0].splitlines()
ips = ""
for ip in ip_lines:
    ips += ip.decode("utf-8") + "\n"


# Creates the text, subject, 'from', and 'to' of the message.
msg = MIMEText(ips)
msg['Subject'] = 'IPs For RaspberryPi on %s' % today.strftime('%b %d %Y')
msg['From'] = "zengjf42@163.com"
msg['To'] = "zengjf42@163.com"

# Sends the message
smtpserver.sendmail(mail_user, [to], msg.as_string())

# Closes the smtp server.
smtpserver.quit()
```

## rc.local

```shell
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# wait dhcp get ip
sleep 10

/bin/autoMail163.py

exit 0
```