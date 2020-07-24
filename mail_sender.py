import os
import json
import smtplib

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.yandex.ru')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

EMAIL_TO = os.environ.get('EMAIL_TO')


def main(**kwargs):
    text = json.dumps(kwargs, indent=2, ensure_ascii=False)
    print("Received: %s" % text)

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    message = "\r\n".join([
        f"From: {EMAIL_HOST_USER}",
        f"To: {EMAIL_TO}",
        "Subject: Serverless Form",
        "",
        str(text)
    ])
    server.set_debuglevel(1)
    server.sendmail(EMAIL_HOST_USER, EMAIL_TO, message)
    server.quit()
    return "Email was sent"
