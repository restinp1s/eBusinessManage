from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app,request
from flaskShop.models import User
from flaskShop.utils.message import to_dict_msg
import functools

def generate_auth_token(uid,expiration):
    s=URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    return s.dumps({'id':uid})

def verify_auth_token(token_str, max_age=3600):
    s=URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        # ✅ loads 时传入 max_age 验证过期时间
        data = s.loads(token_str, max_age=max_age)
    except SignatureExpired:
        return None  # Token 过期
    except BadSignature:
        return None  # Token 无效
    user =User.query.filter_by(id=data['id']).first()
    return user

def login_reqiured(view_func):
    functools.wraps(view_func)
    def verify_token(*args,**kwargs):
        #接受参数
        try:
            token=request.headers['token']
        except Exception:
            return to_dict_msg(1015)
        
        s=URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
        # ✅ loads 时传入 max_age 验证过期时间
            data = s.loads(token)
        except Exception:
            return to_dict_msg(1016)  # Token 过期
        return view_func(*args,**kwargs)
    return verify_token