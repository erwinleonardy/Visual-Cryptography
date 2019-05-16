# Filename: emailerService.py
# Author: Amit Hundal, Harpreet Kang
# Descrption: Defines functions to send asynchronous emails

import inspect
from flask_mail import Message
from threading import Thread

from vsignit.common import Common
from vsignit import app, mail

class EmailerService:
  # Function sends asynchronous emails
  @staticmethod
  def async_email(msg):
    with app.app_context():
      print("Sent!")
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
    print("Recipient email: ")
    print(receiver_email)
    print("\n\n\n\n\n")
    thread = Thread(target=EmailerService.async_email, args=[msg])
    thread.start()

  # function to send email when cheque has been signed by client
  @staticmethod
  def signcheque_email(transaction_no, timestamp, bank_userid, client_userid):
    clientUsername = Common.userid_to_username(client_userid)
    bankUsername = Common.userid_to_username(bank_userid)
    bank_email = Common.userid_to_useremail(bank_userid)
    client_email = Common.userid_to_useremail(client_userid)

    # send email to bank
    bankSubject = "({}) New Cheque from {}".format(bankUsername, clientUsername)
    bankMessage = """
      You have received a new cheque to be processed from {}.

      Transaction Number: {}
      Transaction Time: {}""".format(clientUsername, transaction_no, timestamp)
    EmailerService.send_email(bankUsername, bank_email, bankSubject, bankMessage)

    # send email to client
    clientSubject = "({}) Your cheque has been sent to {}".format(clientUsername, bankUsername)
    clientMessage = """
      Your cheque is currently being processed by {}.

      Transaction Number: {}
      Transaction Time: {}
    
      Your bank will contact you should they have any issue.""".format(bankUsername, transaction_no, timestamp)
    EmailerService.send_email(clientUsername, client_email, clientSubject, clientMessage)
  
  # function to send email after bank determines what to do 
  # with cheque transaction
  @staticmethod
  def transaction_email(transaction_no, client_userid, bank_userid, bank_response):
    clientUsername = Common.userid_to_username(client_userid)
    bankUsername = Common.userid_to_username(bank_userid)
    bank_email = Common.userid_to_useremail(bank_userid)
    client_email = Common.userid_to_useremail(client_userid)

    # send email to bank
    bankSubject = "({}) Outcome of Cheque {}".format(bankUsername, transaction_no)
    bankMessage = """
      You have have just decided to {} a cheque from {}.

      Transaction Number: {}""".format(bank_response, clientUsername, transaction_no)
    EmailerService.send_email(bankUsername, bank_email, bankSubject, bankMessage)

    # send email to client
    clientSubject = "({}) Outcome of Cheque {}".format(clientUsername, transaction_no)
    clientMessage = """
      {} have just decided to {} your cheque.

      Transaction Number: {}
      
      Please do call your bank hotline if you have further enquiries.""".format(bankUsername, bank_response, transaction_no)
    EmailerService.send_email(clientUsername, client_email, clientSubject, clientMessage)