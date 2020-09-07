import datetime

from flask_login import UserMixin 

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from . import db #"." referencia de que se importa del modulo/carpeta

class User(db.Model, UserMixin): #db.model convierete la clase en un modelo/atributosd >> tablas
    #atrubutos/columnas 
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)

    #es necesarios llamar encripted_password a un formulario destinado a un password para poder encriptar la informacion proveniente de este 
    encrypted_password = db.Column(db.String(200), unique = True, nullable = False) #el numero 93 se debe al uso del encriptador que produce un elemento de 93 caracteres
    
    email = db.Column(db.String(100), unique = True, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())
    
    #relaciones
    tasks_user_id = db.relationship('Task', lazy = 'dynamic')#nombre clase/modelo

    def verify_password(self, password):# utriliza para comprar contraseña no encriptada con contraseña encriptada
        return check_password_hash(self.encrypted_password, password) #retorna verdadero o falso

    @property#encriptar contraseña
    def password(self):
        pass

    @password.setter#encriptar contraseña
    def password(self, value):
        self.encrypted_password = generate_password_hash(value)

    def __str__(self):
        return self.username

    @classmethod
    def create_element(cls, username, password, email):#parametros necesarios para crear un usuario
        user = User(username = username, password = password, email = email)
        db.session.add(user)
        db.session.commit()
        return user

    #metodo para saber si un elemento ya existe en una base de datos (validar) (obtener el primer usuario por su username)
    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username = username).first() #nombre del campo a filtrar = valor a utilizar para filtrar

    #obtener un usuario por su id
    @classmethod
    def get_by_id(cls, id):
        return User.query.filter_by(id = id).first() #nombre del campo a filtrar = valor a utilizar para filtrar

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text())
    created_at = db.Column(db.DateTime, default = datetime.datetime.now())

    #relaciones
    tasks_user_id  = db.Column(db.Integer, db.ForeignKey('users.id'))#!!!nombre_tabla!!!.atributo // nombre_tabla =! nombre_clase

    @classmethod
    def create_element(cls, title, description, tasks_user_id):#parametros necesarios para crear un usuario
        task = Task(title = title, description = description, tasks_user_id = tasks_user_id)
        db.session.add(task)
        db.session.commit()
        return task

    @property
    def little_description(self):
        if len(self.description) > 20:
            return self.description[0:19] + "..."
        else:
            return self.description 

    @classmethod
    def get_by_id(cls, id):
        return Task.query.filter_by(id = id).first()

    @classmethod
    def delet_element(cls, id):
        task = Task.get_by_id(id)

        if task is None: #si el elemento no existe
            return False
        else: 
            db.session.delete(task)
            db.session.commit()
            return True
    
    