class Config:
     SECRET_KEY = 'SECRETkEY2'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Mysqlpass123@localhost/project_web'#direccion / usuario / contraseña / direccion db

    #REQUERIDO OBLIGATORIO configuración de acceso para apps menos seguras
    MAIL_SERVER = 'smtp.googlemail.com'# mail_Server - servidor de correos a utiliozar    
    MAIL_PORT = 587# indicar server /(tls) ???? Servidor de correo saliente SMTP​
    MAIL_USE_TLS = True # mail_server
    MAIL_USERNAME = 'carlos.padilla.tsakana@gmail.com' # mail_server
    MAIL_PASSWORD = 'TSAKANApadilla123' #canviar a variables de entorno / decouple >> libreria

#diccionario???
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}