from threading import Thread #async dependance
from flask_mail import Message
from . import mail, app

from flask import current_app, render_template

def send_async_mail(message):
    with app.app_context(): #contexto de la app / sine sto no se podra enviar de manera ascincrona
        mail.send(message)

def welcome_mail(user, mes):
    message = Message('Esto es un mail',
                        sender = current_app.config['MAIL_USERNAME'],
                        recipients = [user.email])

    message.html = render_template('email/welcome.html', user = user, mes = mes)
    
    thread = Thread(target = send_async_mail, args = [message])
    thread.start()