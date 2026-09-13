import os
class Config:
    MYSQL_NAME='root'
    MYSQL_PWD='123321'
    MYSQL_HOST='localhost'
    MYSQL_PORT=3306
    MYSQL_DB='flask_shop'
    MYSQL_CHARSET='utf8mb4'

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_NAME}:{MYSQL_PWD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset={MYSQL_CHARSET}'
    SQLALCHEMY_TRACK_MODIFICATIONS =True

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production' 
    
    ALLOW_IMG = set(['bmp','png','jpg','jpeg','gif'])
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVER_IMG_UPLOAD = os.path.join(BASE_DIR,'flaskShop','static','img')

class DevelopmentConfig(Config):
    DEBUG=True   

class ProductionConfig(Config):
    pass  

config_map={
    'develop':DevelopmentConfig,
    'product':ProductionConfig
}