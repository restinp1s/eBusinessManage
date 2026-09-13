from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config_map
from flask_cors import CORS

db =SQLAlchemy()
migrate = Migrate()
def create_app(config_name):

    app = Flask(__name__)


    CORS(
        app,
        supports_credentials=True
    )


    obj = config_map.get(config_name)

    app.config.from_object(obj)


    db.init_app(app)

    migrate.init_app(app,db)



    from flaskShop.user import user
    from flaskShop.menu import menu
    from flaskShop.role import role
    from flaskShop.category import category
    from flaskShop.category import attribute
    from flaskShop.goods import goods
    from flaskShop.order import order
    
    app.register_blueprint(user)

    app.register_blueprint(menu)

    app.register_blueprint(role)

    app.register_blueprint(category)

    app.register_blueprint(attribute)

    app.register_blueprint(goods)

    app.register_blueprint(order)
    print(app.url_map)

    return app

    
