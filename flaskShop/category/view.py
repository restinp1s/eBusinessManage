from flaskShop.category import category,category_api,attribute,attribute_api
from flask import request
from flaskShop import models,db
from flask_restful import Resource
import re
from flaskShop.utils.message import to_dict_msg
class Category(Resource):
    def get(self):
        try:
            cid = request.args.get('cid')
            c = models.Category.query.get(cid)
            if c:
                return to_dict_msg(200,c.to_dict(),'获取商品分类成功！')
            else:
                return to_dict_msg(1001)
        except Exception: 
            return to_dict_msg(1021)

    def post(self):
        try:
            name = request.form.get('name') if request.form.get('name') else ''
            level = int(request.form.get('level')) if request.form.get('level') else None
            pid = int(request.form.get('pid')) if request.form.get('pid') else 0

            if all([name,level]):
                if pid:
                    c = models.Category(name=name,level=level,pid=pid)
                else:
                    c = models.Category(name=name,level=level)
                db.session.add(c)
                db.session.commit()
                return to_dict_msg(200,msg='增加商品分类成功！')
            return to_dict_msg(1001)
        except Exception as e:
            return to_dict_msg(1021)

    def put(self):
        try:
            cid = request.form.get('cid')
            name = request.form.get('name')
            c = models.Category.query.get(cid)
            if c:
                c.name = name
                db.session.commit()
                return to_dict_msg(200,msg='更新商品分类成功！')
            return to_dict_msg(1001)
        except Exception:
            return to_dict_msg(1021)
        
    def delete(self):
        cid = request.form.get('cid')
        c = models.Category.query.get(cid)
        if c:
            db.session.delete(c)
            db.session.commit()
            return to_dict_msg(200,msg='删除商品分类成功！')
        return to_dict_msg(1001)

category_api.add_resource(Category,'/category')
    
@category.route('/category_list')
def get_category_list():
    if request.args.get('level') and int(request.args.get('level'))<=3:
        level = int(request.args.get('level'))
    else:
        level = 0

    pnum = int(request.args.get('pnum')) if request.args.get('pnum') else 0
    psize = int(request.args.get('psize')) if request.args.get('psize') else 0

    cate_list = []  #新建一个列表，将原类对象数据以字典形式拷贝至新列表
    base_query = models.Category.query.filter(models.Category.level == 1)

    if all([pnum,psize]):
        categories = base_query.paginate(page=pnum,per_page=psize)  #这段代码为更新版本
        if level:
            cate_list =get_tree(categories.items,level,True)
        else:
            cate_list =get_tree(categories.items,level,False)

        data={
            'pnum':pnum,
            'psize':psize,
            'total':categories.total,
            'data':cate_list
        }
        return to_dict_msg(200,data,'获取商品分类列表成功！')    
    else:
        categories = base_query.all()
        if level:
            cate_list = get_tree(categories,level,True)
        else:
            # for c in categories:
            #     f_dict = c.to_dict()
            #     f_dict['children'] = []
            #     for sc in c.children:
            #         s_dict = sc.to_dict()
            #         s_dict['children'] = []
            #         for tc in sc.children:
            #             s_dict['children'].append(tc.to_dict())
            #         f_dict(s_dict)
            #     cate_list.append(f_dict)
            cate_list = get_tree(categories,level,False)
        return to_dict_msg(200,{'data':cate_list},'获取商品分类列表成功！')

def get_tree(info_list,level,flag):
    info_dict = []
    if info_list:
        for i in info_list:
            i_dict = i.to_dict()
            if flag:
                if i.level < level:
                    i_dict['children'] = get_tree(i.children,level,flag)
            else:
                if i.level !=3:
                    i_dict['children'] = get_tree(i.children,level,flag)
            info_dict.append(i_dict)
    return info_dict
        
class Attribute(Resource):
    def post(self):
        try:
            name = request.form.get('name')
            cid = request.form.get('cid')
            _type = request.form.get('_type')
            val = request.form.get('val')

            if all([name,cid,_type]):
                if val:
                    attr = models.Attribute(name=name,cid=int(cid),_type=_type,val=val)
                else:
                    attr = models.Attribute(name=name,cid=int(cid),_type=_type)

                db.session.add(attr)
                db.session.commit()
                return to_dict_msg(200,msg="增加分类参数成功！")
            else:
                return to_dict_msg(1001)
            
        except Exception as e:
            return to_dict_msg(1021)
        
    def get(self):
        id = request.args.get('id')
        attr =models.Attribute.query.get(id)
        if attr:
            return to_dict_msg(200,attr.to_dict(),msg='获取分类参数成功！')
        else:
            return to_dict_msg(1021)
        
    def put(self):
        try:
            id = request.form.get('id')
            name = request.form.get('name')
            val = request.form.get('val')
            cid = int(request.form.get('cid')) if request.form.get('cid') else 0
            if all([id,name,cid]):
                attr = models.Attribute.query.get(id)
                if attr:
                    attr.name = name
                    attr.val = val
                    attr.cid = cid
                    db.session.commit()
                    return to_dict_msg(200,msg='更新数据成功！')
                else:
                    return to_dict_msg(1001)
            else:
                return to_dict_msg(1001)
        except Exception:
            return to_dict_msg(1021)
        
    def delete(self):
        id = request.form.get('id')
        attr = models.Attribute.query.get(id)
        if attr:
            db.session.delete(attr)
            db.session.commit()
            return to_dict_msg(200,attr.to_dict(),msg='删除分类参数成功！')
        else:
            return to_dict_msg(1001)
        

attribute_api.add_resource(Attribute,'/attribute')

@attribute.route('/attr_list')
def get_attr_list():
    cid = request.args.get('cid')
    _type = request.args.get('_type')

    print('cid:', cid)
    print('_type:', _type)

    if all([cid, _type]):
        cate = models.Category.query.get(cid)

        print('cate:', cate)

        if cate:
            print('cate.attrs:', cate.attrs)

            for a in cate.attrs:
                print(
                    '属性:',
                    a.id,
                    a.name,
                    a._type,
                    a.val
                )

            if _type == 'static':
                attr_list = [
                    a.to_dict()
                    for a in cate.attrs
                    if a._type == 'static'
                ]
            else:
                attr_list = [
                    a.to_dict()
                    for a in cate.attrs
                    if a._type == 'dynamic'
                ]

            print('attr_list:', attr_list)

            return to_dict_msg(
                200,
                attr_list,
                msg='获取分类属性列表成功！'
            )
        else:
            return to_dict_msg(1001)
    else:
        return to_dict_msg(1001)
    
from sqlalchemy import func
    
@attribute.route('/cate_group_level')
def get_cate_group_by_level():
    #group_data = models.Category.query.group_by(models.Category.level).all()
    group_data = db.session.query(models.Category.level,func.count(1).label('count')).group_by(models.Category.level).having(models.Category.level > 0).all()
    data ={
        'name':'数量',
        'xAxis':[f'{g[0]}级分类' for g in group_data],
        'series_data':[g[1] for g in group_data]
    }
    return to_dict_msg(200,data)