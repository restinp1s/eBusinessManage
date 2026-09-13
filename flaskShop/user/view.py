from flaskShop.user import user,user_api
from flask import request
from flaskShop import models,db
from flask_restful import Resource,reqparse
import re
from flaskShop.utils.message import to_dict_msg
from flaskShop.utils.tokens import generate_auth_token,verify_auth_token,login_reqiured
from werkzeug.security import generate_password_hash

@user.route('/')
def index():
    return 'hello!! user'

class User(Resource):
    def get(self):
        try:
            id = request.args.get('id')
            usr = models.User.query.filter_by(id=id).first()
            if usr:
                return to_dict_msg(200,usr.to_dict(),'获取用户成功')
            else:
                return to_dict_msg(200,[],'获取失败')
        except Exception as e:
            print("错误信息:", e)
            return to_dict_msg(1001)
    def post(self):

        data = request.get_json()


        print("================")
        print("进入新增用户接口")
        print("Content-Type:", request.content_type)
        print("原始数据:", request.data)
        print("================")


        if data is None:

            return {
                "status":1001,
                "msg":"JSON解析失败"
            }


        name = data.get('name')
        pwd = data.get('pwd')
        nick_name = data.get('nick_name')
        phone = data.get('phone')
        email = data.get('email')
        #验证数据完整性
        if not all([name,pwd,phone,email]):
            return to_dict_msg(1001)
        if len(name) <2:
            return to_dict_msg(1011)
        if len(pwd) <2:
            return to_dict_msg(1012)
        if not re.match(r'^1[345678]\d{9}$',phone):
            return to_dict_msg(1013)
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',email):
            return to_dict_msg(1014)
        try:
            rid = int(data.get('role_name')) if data.get('role_name') else 0
            user =models.User(name =name,password =pwd,nick_name=nick_name,phone=phone,email=email,rid=rid)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                'status':1000,
                'msg':str(e)
            }
        return to_dict_msg(200)
    
    def put(self):

        try:

            # 接收Vue3 axios JSON数据
            data = request.get_json()


            print("修改用户数据:", data)


            id = data.get('id')

            pwd = data.get('pwd')

            email = data.get('email')

            phone = data.get('phone')

            rid = int(data.get('role_name')) if data.get('role_name') else 0



            # 参数判断

            if not id:

                return to_dict_msg(
                    1001,
                    msg="用户ID不能为空"
                )



            # 查询用户

            usr = models.User.query.get(id)



            if usr:


                # 修改密码

                if pwd:
                    usr.pwd = generate_password_hash(pwd)



                # 修改邮箱

                if email:

                    usr.email = email



                # 修改电话

                if phone:

                    usr.phone = phone

                if rid:

                    usr.rid = int(rid)



                # 提交事务

                db.session.commit()



                return to_dict_msg(
                    200,
                    msg='用户信息修改成功'
                )


            else:


                return to_dict_msg(
                    1017,
                    msg='用户不存在'
                )


        except Exception as e:


            print("修改用户错误:", e)


            db.session.rollback()


            return to_dict_msg(
                1001,
                msg='修改失败'
            )
        
    def delete(self):

        try:


            data=request.get_json()


            print(
                "删除用户:",
                data
            )


            id=data.get('id')



            usr=models.User.query.get(id)



            if usr:


                db.session.delete(usr)


                db.session.commit()



                return to_dict_msg(
                    200,
                    msg="删除成功"
                )



            else:


                return to_dict_msg(
                    1019,
                    msg="用户不存在"
                )


        except Exception as e:


            print(e)


            db.session.rollback()


            return to_dict_msg(
                1001,
                msg="删除失败"
            )
        

user_api.add_resource(User,'/user')

# class UserList(Resource):

#     def get(self):

#         parser = reqparse.RequestParser()

#         parser.add_argument(
#             'name',
#             type=str,
#             location='args'
#         )

#         parser.add_argument(
#             'pnum',
#             type=int,
#             default=1,
#             location='args'
#         )

#         parser.add_argument(
#             'psize',
#             type=int,
#             default=4,
#             location='args'
#         )

#         args = parser.parse_args()

#         name = args.get('name')
#         pnum = args.get('pnum')
#         psize = args.get('psize')

#         if name:

#             users_pn = models.User.query.filter(
#                 models.User.name.like(
#                     f'%{name}%'
#                 )
#             ).paginate(
#                 page=pnum,
#                 per_page=psize
#             )

#         else:

#             users_pn = models.User.query.paginate(
#                 page=pnum,
#                 per_page=psize
#             )

#         data = {

#             "pnum": pnum,

#             "total": users_pn.total,

#             "users": [
#                 u.to_dict()
#                 for u in users_pn.items
#             ]

#         }

#         return to_dict_msg(
#             200,
#             data,
#             "获取用户列表成功"
#         )
class UserList(Resource):

    def get(self):

        try:

            # 当前页
            pnum = int(request.args.get('pnum', 1))

            # 每页数量
            psize = int(request.args.get('psize', 2))


            # 查询全部用户对象(不是all)
            query = models.User.query.order_by(
                models.User.id.asc()
            )


            # 总数量
            total = query.count()


            # 分页查询
            users = query.offset(
                (pnum - 1) * psize
            ).limit(
                psize
            ).all()


            data = []


            for user in users:

                data.append(
                    user.to_dict()
                )


            return to_dict_msg(
                200,
                {
                    "pnum": pnum,

                    "psize": psize,

                    "total": total,

                    "users": data
                },

                "获取用户列表成功"
            )


        except Exception as e:

            print("错误:", e)

            return to_dict_msg(1001)
    
user_api.add_resource(UserList,'/user_list')

@user.route('/login',methods=['POST'])
def login():
        name =request.form.get('name')
        pwd =request.form.get('pwd')

        if not all([name,pwd]):
                    return {'status':1000,'msg':'数据不完整'}
        if len(name) >1:
            user =models.User.query.filter_by(name=name).first()
            if user:
                if user.check_password(pwd):
                        token=generate_auth_token(user.id,1000)
                        return {'status':200,'data':{'token':token}}                        
        return to_dict_msg(1001)

# 1表单验证
# 2提交用户名密码到 Flask 后端
# 3判断登录结果
# 4保存 token
# 5跳转主页