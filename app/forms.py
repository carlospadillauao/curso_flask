from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField, TextAreaField

from .models import *

def validador_nuevo(form, field): # funciona a de resivir el formulario y cxampo a validar (validar. reutilizable en otros metodos)
    if field.data == 'codi' or field.data == 'CODI':
        raise validators.ValidationError('Usuario no permitido')#lebantar exepcion

class LoginForm(Form):
    username = StringField('Username',[
        validators.length(min = 4, max = 50, message = 'min 4 maximo 50 digitos')
    ])
    password = PasswordField('Password',[
        validators.Required()
    ])

class RegisterForm(Form):
    username = StringField('Username',[
        validators.length(min = 4, max = 50, message = 'min 4 maximo 50 digitos'),
        validador_nuevo #validador personalizado
    ])
    password = PasswordField('Password',[
        validators.Required()
    ])
    email = StringField('email',[
        validators.Required()
    ])

    def validate_username(self, username): #metodo para validar un campo especifico (validar. no reutilizable)
        if User.get_by_username(username.data):
            raise validators.ValidationError('usuario ya registrado')

class TaskForm(Form):
    title = StringField('Titulo', [
        validators.length(min = 4, max = 50, message = 'Titulo fuera de rango'),
        validators.DataRequired(message = 'Este campo es requerido')
    ])
    description = TextAreaField('Descripcion',[
        validators.DataRequired(message = 'Este campo es requerido')
    ], render_kw = {'rows': 5}) #rows >> espacion del texto

