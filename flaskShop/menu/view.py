from flaskShop.menu import menu,menu_api
from flask import request
from flaskShop import models,db
from flask_restful import Resource
import re
from flaskShop.utils.message import to_dict_msg

class Menu(Resource):

    def get(self):

        type_ = request.args.get('type')

        menu_list = []


        if type_ == 'list':

            menus = models.Menu.query.filter(
                models.Menu.level != 0
            ).all()


            menu_list = [
                m.to_dict()
                for m in menus
            ]


        else:

            menus = models.Menu.query.filter(
                models.Menu.level == 1
            ).all()


            for menu in menus:


                first = menu.to_dict()

                first['children'] = []


                for child in menu.children:


                    second = child.to_dict()


                    second['children'] = (
                        child.get_child_list()
                    )


                    first['children'].append(
                        second
                    )


                menu_list.append(first)


        return to_dict_msg(
            200,
            menu_list,
            "获取菜单成功"
        )
    
menu_api.add_resource(
    Menu,
    '/menu'
)