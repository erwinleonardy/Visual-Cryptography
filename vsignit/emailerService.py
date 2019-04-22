from vsignit import app, mail
from flask_mail import Message
from threading import Thread

class EmailerService:
  @staticmethod
  def async_email(msg):
    with app.app_context():
        mail.send(msg)

  @staticmethod
  def sendEmail(username, receiver_email, subject, msg_body):
    body =  """\
      Hi, {}!\n""".format(username)
    body += msg_body
    body += """
    
      Thank you for choosing VSignIt as your preferred encryption method.
      
      (This is an auto-generated email. Please do not reply directly to this email.)
      
      ***** DISCLAIMER *****
      This email and any attachments thereto are intended for the sole use of the recipient(s) named above and 
      may contain information that is confidential and/or proprietary to the VSingIt Group. If you have received 
      this email in error, please notify the sender immediately and delete it.
      
      Best Regards,
      VSignIt Admin Team
    """

    msg = Message(subject=subject, body=body, recipients=[receiver_email])
    thread = Thread(target=EmailerService.async_email, args=[msg])
    thread.start()


    # text += """!\

    # Here is your share! Please ensure that you keep this file safe :)

    # Thank you for choosing VSignIt as your preferred encryption method.

    # (This is an auto-generated email. Please do not reply directly to this email.)

    # ***** DISCLAIMER *****
    # This email and any attachments thereto are intended for the sole use of the recipient(s) named above and 
    # may contain information that is confidential and/or proprietary to the VSingIt Group. If you have received 
    # this email in error, please notify the sender immediately and delete it.

    # Best Regards,
    # VSignIt Admin Team"""