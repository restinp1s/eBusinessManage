from flask import Blueprint
from flask_restful import Api

role =Blueprint('role',__name__, url_prefix='/role')
role_api=Api(role)
from flaskShop.role import view