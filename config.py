class Config:
     SECRET_KEY = 'SECRETkEY2'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Mysqlpass123@localhost/project_web'#direccion / usuario / contraseña / direccion db

#diccionario???
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}