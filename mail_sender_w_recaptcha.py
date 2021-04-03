import os
import json
import smtplib
from urllib import request, parse

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.yandex.ru')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

EMAIL_TO = os.environ.get('EMAIL_TO')

RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY')


def is_captcha_challenge_succeed(response_token):
    data = parse.urlencode({
        'secret': RECAPTCHA_SECRET_KEY,
        'response': response_token,
    }).encode()
    req = request.Request('https://www.google.com/recaptcha/api/siteverify', data=data)
    resp_data = json.load(request.urlopen(req))
    return resp_data.get('success') or False


def format_email(**kwargs):
    return json.dumps(kwargs, indent=2, ensure_ascii=False)


def send_email(text):
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


def main(**kwargs):
    if is_captcha_challenge_succeed(kwargs.pop('g-recaptcha-response')):
        text = format_email(**kwargs)
        print(f'Sending """{text}"""')
        send_email(text)
        return "Email was sent"
    return "CAPTCHA challenge failed"
