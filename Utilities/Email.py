from flask import render_template
from flask_mail import Message


def sendEmailText(reciverMail, subject, content):
    from app import mail
    msg = Message(subject, sender='hydrasneaker@gmail.com', recipients=[reciverMail])
    msg.body = content
    mail.send(msg)


def sendEmailTemplate(reciverMail, subject, template, **kwargs):
    from app import mail
    htmlContent = render_template(template, **kwargs)
    msg = Message(subject, sender='hydrasneaker@gmail.com', recipients=[reciverMail])
    msg.html = htmlContent
    mail.send(msg)
