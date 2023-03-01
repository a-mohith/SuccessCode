import boto3
import datetime
import smtplib
from email.mime.text import MIMEText

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('my-report-bucket')

    # Empty the bucket
    for obj in bucket.objects.all():
        obj.delete()

    # Check if there are any lingering files
    count = sum(1 for _ in bucket.objects.all())
    if count > 0:
        message = f"Lingering files found in my-report-bucket ({count} files)"
        send_email(message)
    
def send_email(message):
    email_sender = "sender@example.com"
    email_recipient = "recipient@example.com"
    email_subject = f"Lingering files found in my-report-bucket ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
    email_body = message

    msg = MIMEText(email_body)
    msg['Subject'] = email_subject
    msg['From'] = email_sender
    msg['To'] = email_recipient

    s = smtplib.SMTP('smtp.example.com')
    s.sendmail(email_sender, [email_recipient], msg.as_string())
    s.quit()
