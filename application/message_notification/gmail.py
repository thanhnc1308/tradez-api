import os
import smtplib
from email.message import EmailMessage

os.environ['EMAIL_USER'] = 'montoson138@gmail.com'
os.environ['EMAIL_PASSWORD'] = '12345678@Abc'

EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# def read_creds():
#     user = password = ''
#     with open('credentials.txt', 'r') as f:
#         file = f.readlines()
#         user = file[0].strip()
#         password = file[1].strip()
#     return user, password

# EMAIL_USER, EMAIL_PASSWORD = read_creds()

test_msg = """\
        <!DOCTYPE html>
        <html>
            <body>
                <h1 style="color:SlateGray;">This is an HTML Email!</h1>
            </body>
        </html>
        """

def send_email(receivers, msg=test_msg):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)

        email_message = EmailMessage()
        email_message['Subject'] = 'Notification Alert From Trading Assistant'
        email_message['From'] = EMAIL_USER
        email_message['To'] = ','.join(receivers)
        email_message.set_content(msg)
        # msg.add_alternative(msg, subtype='html')

        smtp.send_message(email_message)
        smtp.quit()

def send_email_html(receivers, html):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)

        email_message = EmailMessage()
        email_message['Subject'] = 'Test subject'
        email_message['From'] = EMAIL_USER
        email_message['To'] = ','.join(receivers)
        email_message.add_alternative(html, subtype='html')

        smtp.send_message(email_message)
        smtp.quit()

# send_email_html(['thanhcongaone@gmail.com'], msg)
