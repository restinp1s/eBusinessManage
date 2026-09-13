from flaskShop import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class BaseModel:
    create_time =db.Column(db.DateTime,default=datetime.now)
    update_time =db.Column(db.DateTime,default=datetime.now,onupdate =datetime.now)

class User(db.Model,BaseModel):
    __tablename__ ='t_user'
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    pwd = db.Column(db.String(256))
    nick_name =db.Column(db.String(32))
    phone = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(32))

    rid =db.Column(db.Integer,db.ForeignKey('t_role.id'),default=1)

    #加密措施,装饰器
    @property
    def password(self):
        return self.pwd
    
    @password.setter
    def password(self,t_pwd):
        self.pwd =generate_password_hash(t_pwd)

    def check_password(self,t_pwd):
        return check_password_hash(self.pwd,t_pwd) #库密码和传递进来的密码
    
    def to_dict(self):
        return {
        'id': self.id, 
        'name': self.name, 
        'nick_name': self.nick_name, 
        'phone': self.phone, 
        'email': self.email,
        'role_name':self.role.name if self.role else ''
        }
#第三张关联表
trm = db.Table('t_role_menu',
        db.Column('rid',db.Integer,db.ForeignKey('t_role.id')), 
        db.Column('mid',db.Integer,db.ForeignKey('t_menu.id'))        
    )

class Menu(db.Model):
    # 菜单字典
    __tablename__ = 't_menu' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    level = db.Column(db.Integer)
    path = db.Column(db.String(32))
    pid = db.Column(db.Integer,db.ForeignKey('t_menu.id'))
    children = db.relationship('Menu')

    roles = db.relationship('Role',secondary =trm) #引入第三张表的外键

    def to_dict(self):
        return {
        'id': self.id, 
        'name': self.name, 
        'level': self.level, 
        'path': self.path, 
        'pid': self.pid
        }

    def get_child_list(self):
        # 获取子菜单里的对象
        obj_child = self.children
        data = []
        for o in obj_child:
            data.append(o.to_dict())
        return data
    
class Role(db.Model):
    # 角色权限字典
    __tablename__ = 't_role' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32),nullable=False)
    desc = db.Column(db.String(64))

    users = db.relationship('User',backref ='role') #关联获取User全部属性,并且把Role的信息回馈给User
    menus = db.relationship('Menu',secondary =trm) #引入第三张表的外键

    def to_dict(self):
        return {
        'id': self.id, 
        'name': self.name, 
        'desc': self.desc,
        'menu':self.get_menu_dict()
        }

    def get_menu_dict(self):
        menu_list =[]
        menus = sorted(self.menus,key=lambda temp:temp.id)
        for m in menus:
            if m.level == 1:
                first_dict =m.to_dict()
                first_dict['children'] =[]
                for s in menus:
                    print(
                    '检查子菜单:',
                    s.name,
                    s.level,
                    s.pid
                    )
                    if s.level == 2 and s.pid == m.id:
                        #当前子节点的父级等于当前的一级的id
                        first_dict['children'].append(s.to_dict())
                menu_list.append(first_dict)
        return menu_list


class Category(db.Model):
    __tablename__ = 't_category' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32),nullable=False)
    level = db.Column(db.Integer)
    pid = db.Column(db.Integer,db.ForeignKey('t_category.id')) #自关联本表
    attrs = db.relationship('Attribute',backref='category')

    children = db.relationship('Category')

      # 同一个父分类下面，分类名称不能重复
    __table_args__ = (
        db.UniqueConstraint(
            'pid',
            'name',
            name='uq_category_pid_name'
        ),
    )


    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'level':self.level,
            'pid':self.pid
        }
    
class Attribute(db.Model):
    __tablename__ = 't_attribute' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    val = db.Column(db.String(255))
    cid = db.Column(db.Integer,db.ForeignKey('t_category.id'))
    _type = db.Column(db.Enum('static','dynamic'))

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'val':self.val,
            'cid':self.cid,
            'type':self._type
        }
    
class Goods(db.Model):
    __tablename__ = 't_goods' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Float)
    number = db.Column(db.Integer)
    introduce = db.Column(db.Text)
    big_logo = db.Column(db.String(256))
    small_logo = db.Column(db.String(256))
    state = db.Column(db.Integer) #0 未通过 1 审核中 2 已通过
    is_onsale = db.Column(db.Integer) #是否促销
    hot_number = db.Column(db.Integer) #促销数量
    weight = db.Column(db.Integer) #推送权重
    cid_one = db.Column(db.Integer,db.ForeignKey('t_category.id')) #分类属性
    cid_two = db.Column(db.Integer,db.ForeignKey('t_category.id'))
    cid_three = db.Column(db.Integer,db.ForeignKey('t_category.id'))

    category = db.relationship('Category',foreign_keys=[cid_three])
    
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'price':self.price,
            'number':self.number,
            'introduce':self.introduce,
            'big_logo':self.big_logo,
            'small_logo':self.small_logo,
            'state':self.state,
            'is_onsale':self.is_onsale,
            'hot_number':self.hot_number,
            'weight':self.weight,
            'cid_one':self.cid_one,
            'cid_two':self.cid_two,
            'cid_three':self.cid_three,
            'attrs':[a.to_dict() for a in self.category.attrs]
        }
    
class Picture(db.Model):
    __tablename__ = 't_picture' 
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(512))
    gid = db.Column(db.Integer,db.ForeignKey('t_goods.id'))

class GoodsAttr(db.Model):
    #第三方表，一个商品可以有多个属性，一个属性可以对应多个商品
    __tablename__ = 't_goods_attr'
    gid = db.Column(db.Integer,db.ForeignKey('t_goods.id'),primary_key=True)
    aid = db.Column(db.Integer,db.ForeignKey('t_attribute.id'),primary_key=True)
    #定制一个新的商品，新增Attr属性值
    val = db.Column(db.String(255))
    _type = db.Column(db.String(8))
    
class Order(db.Model,BaseModel):
#买家和卖家是否为同一个数据库系统
    __tablename__ = 't_order'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer,db.ForeignKey('t_user.id'))
    price = db.Column(db.Float)
    number = db.Column(db.Integer)
    pay_status = db.Column(db.Integer) #0,1
    is_send = db.Column(db.Integer)
    ticket_title =db.Column(db.String(32))
    ticket_company =db.Column(db.String(32))
    ticket_content =db.Column(db.String(512))
    addrs =db.Column(db.String(128))

    user = db.relationship('User',foreign_keys=[uid])
    order_detial = db.relationship('OrderDetail',backref='order')
    express = db.relationship('Express',backref='order')

    def to_dict(self):
        return {
            'id':self.id,
            'uid':self.uid,
            'uname':self.user.name,
            'price':self.price,
            'number':self.number,
            'pay_status':self.pay_status,
            'is_send':self.is_send,
            'ticket_title':self.ticket_title,
            'ticket_company':self.ticket_company,
            'ticket_content':self.ticket_content,
            'addrs':self.addrs
        }


class OrderDetail(db.Model):
    #购买物品清单
    __tablename__ = 't_order_detail'
    gid = db.Column(db.Integer,db.ForeignKey('t_goods.id'),primary_key=True)
    oid = db.Column(db.Integer,db.ForeignKey('t_order.id'),primary_key=True)
    number = db.Column(db.Integer)
    price = db.Column(db.Float)
    total_price = db.Column(db.Float)

class Express(db.Model):
    __tablename__ = 't_express'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128))
    update_time = db.Column(db.String(32))
    oid = db.Column(db.Integer,db.ForeignKey('t_order.id'))

    def to_dict(self):
        return {
            'id':self.id,
            'content':self.content,
            'update_time':self.update_time,
            'oid':self.oid
        }


