import email, smtplib, ssl, os

from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def emailer (receiver_email, filename):
	sender_email = "4youreyesonlyservice@gmail.com"

	password = "123erwin"

	message = MIMEMultipart("alternative")

	message["Subject"] = "Your VSignIt Share"
	message["From"] = sender_email
	message["To"] = receiver_email
	username = receiver_email.split("@")[0]

	# create mail here

	text = """\
	Hi, """ + username

	text += """!\
	

	Here is your share! Please ensure that you keep this file safe :)
	
	Thank you for choosing VSignIt as your preferred encryption method.

	(This is an auto-generated email. Please do not reply directly to this email.)

	***** DISCLAIMER *****
	This email and any attachments thereto are intended for the sole use of the recipient(s) named above and 
	may contain information that is confidential and/or proprietary to the VSingIt Group. If you have received 
	this email in error, please notify the sender immediately and delete it.
	
	Best Regards,
	VSignIt Admin Team"""

	part1 = MIMEText(text, "plain")
	#part2 = MIMEText(html, "html")

	message.attach(part1)
	#message.attach(part2)

	img_data = open(filename, 'rb').read()
	part3 = MIMEImage(img_data, name=os.path.basename(filename))

	message.attach(part3)

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(
			sender_email, receiver_email, message.as_string()
			)
