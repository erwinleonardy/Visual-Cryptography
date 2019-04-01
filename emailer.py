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

	# create mail here

	text = """\
	Hi,

	Thank You for Using VSignIt!
	
	Here is your share!"""


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
