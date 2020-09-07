from flask import Flask
from flask_bootstrap import Bootstrap#import/permite el uso de bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy#coneccion con base de datos
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy()#coneccion con base de datos
csrf = CSRFProtect()
bootstrap = Bootstrap()#instancia/permite el uso de bootstrap
login_manager = LoginManager()

from .views import page 
from .models import *
from .consts import *

def create_app(config):
    app.config.from_object(config)
    
    app.register_blueprint(page)
    
    csrf.init_app(app)
    bootstrap.init_app(app)#asignacion/permite el uso de bootstrap 
    
    login_manager.init_app(app)
    login_manager.login_view = '.login' #si un usuario no logueado intenta ingresar a una pagina restringida sera redirigido a esta direccion
    login_manager.login_message = LOGIN_REQUIRED

    with app.app_context():
        db.init_app(app)#coneccion con base de datos
        db.create_all()#crear todas las tablas en la db
    return app