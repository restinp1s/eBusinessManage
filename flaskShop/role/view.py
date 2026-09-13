from flaskShop.role import role,role_api
from flask import request
from flaskShop import models,db
from flask_restful import Resource
import re
from flaskShop.utils.message import to_dict_msg

class Role(Resource):
    def get(self):
        try:
            role_list =[]
            roles =models.Role.query.all()
            role_list =[r.to_dict() for r in roles]
            return to_dict_msg(200,role_list,'获取角色列表成功')
        except Exception:
            return to_dict_msg(1001)
        
    def post(self):
        name=request.form.get('name')
        desc=request.form.get('desc')
        try:
            if name:
                role = models.Role(name=name,desc=desc)
                db.session.add(role)
                db.session.commit()
                return to_dict_msg(200,msg='添加角色成功')
            else:
                return to_dict_msg(1001)
            
        except Exception:
            return to_dict_msg(1001)
        
    def delete(self):
        try:
            id =int(request.form.get('id'))
            r =models.Role.query.get(id)
            if r:
                db.session.delete(r)
                db.session.commit()
                return to_dict_msg(200,msg='删除角色成功')
            else:
                return to_dict_msg(1001)
            
        except Exception:
            return to_dict_msg(1001)
            
    def put(self):
        try:
            id =int(request.form.get('id'))
            name = request.form.get('name').strip() if request.form.get('name') else ''
            desc = request.form.get('desc').strip() if request.form.get('desc') else ''
            if name:
                r = models.Role.query.get(id)
                if r:
                    r.name = name
                    r.desc = desc
                    db.session.commit()
                    return to_dict_msg(200,msg='修改角色成功')
                else:
                    return to_dict_msg(1020)
            else:
                return to_dict_msg(1001)
            
        except Exception:
            return to_dict_msg(1001)

class RoleMenu(Resource):

    def delete(self):

        try:

            rid = request.args.get('rid')

            mid = request.args.get('mid')


            rm = models.trm.delete().where(
                models.trm.c.rid == rid,
                models.trm.c.mid == mid
            )


            db.session.execute(rm)

            db.session.commit()


            return to_dict_msg(
                200,
                msg='删除权限成功'
            )


        except Exception as e:

            db.session.rollback()

            return to_dict_msg(
                1001,
                msg=str(e)
            )        


# 注册角色接口
role_api.add_resource(
    Role,
    '/role_list'
)


# 注册角色权限删除接口
role_api.add_resource(
    RoleMenu,
    '/menu'
)

@role.route(
    '/set_menu/<int:rid>',
    methods=['POST']
)
def set_menu(rid):
    print("进入set_menu")
    print(request.form)

    try:

        role_obj=models.Role.query.get(rid)

        mids=request.form.get('mids','')


        if not role_obj:

            return to_dict_msg(1017)


        role_obj.menus=[]


        if mids:

            for mid in mids.split(','):

                menu=models.Menu.query.get(
                    int(mid)
                )

                if menu:

                    role_obj.menus.append(menu)


        db.session.commit()


        return to_dict_msg(
            200,
            msg='分配权限成功'
        )


    except Exception as e:

        db.session.rollback()

        return to_dict_msg(
            1001,
            msg=str(e)
        )