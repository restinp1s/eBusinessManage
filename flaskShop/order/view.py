from flaskShop.order import order,order_api
from flask import request
from flaskShop import models,db
from flask_restful import Resource
import re
from flaskShop.utils.message import to_dict_msg

@order.route('/order_list')
def order_list():
    id = request.args.get('id') #通过主键获取
    if id:
        order = models.Order.query.get(id)
        if order:
            return to_dict_msg(200,order.to_dict(),msg='获取订单成功！')
        else:
            return to_dict_msg(1001)
    orders = models.Order.query.all()
    return to_dict_msg(200,[o.to_dict() for o in orders],msg='获取订单列表成功！')

@order.route('/express')
def get_express():
    oid = request.args.get('oid')
    if oid:
        exps = models.Express.query.filter(models.Express.oid == oid).order_by(models.Express.update_time.desc())
        return to_dict_msg(200,[e.to_dict() for e in exps])
    else:
        return to_dict_msg(1001)
    
