# Filename: emailerService.py
# Author: Amit Hundal, Harpreet Kang 
# Descrption: Defines functions to send asynchronous emails

import inspect
from flask_mail import Message
from threading import Thread

from vsignit import app, mail

class EmailerService:
  # Function sends asynchronous emails
  @staticmethod
  def async_email(msg):
    with app.app_context():
      mail.send(msg)

  # function to format emails
  @staticmethod
  def send_email(username, receiver_email, subject, body):
    msg_body =  """\
      Hi, {}!\n""".format(username)
    msg_body += body
    msg_body += """
    
      Thank you for choosing VSignIt as your preferred encryption method.
      
      (This is an auto-generated email. Please do not reply directly to this email.)
      
      ***** DISCLAIMER *****
      This email and any attachments thereto are intended for the sole use of the recipient(s) named above and 
      may contain information that is confidential and/or proprietary to the VSingIt Group. If you have received 
      this email in error, please notify the sender immediately and delete it.
      
      Best Regards,
      VSignIt Admin Team
    """

    msg = Message(subject=subject, body=inspect.cleandoc(msg_body), recipients=[receiver_email])
    thread = Thread(target=EmailerService.async_email, args=[msg])
    thread.start()
