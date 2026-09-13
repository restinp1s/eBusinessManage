#状态码字典
status_msg={
    200:'成功！',
    1001:'数据不完整',
    1011:'用户名不规范',
    1012:'密码不规范',
    1013:'手机号不规范',
    1014:'邮箱不规范',
    1015:'请先登录',
    1016:'token无效',
    1017:'修改用户出错',
    1019:'删除失败',
    1020:'没有传入ID',
    1021:'异常错误',
    1022:'没有上传文件！',
    1023:'文件格式不规范！',
    10001:'用户名或密码错误！！'
}

def to_dict_msg(status=200,data=None,msg=None):
    return {
        'status':status,
        'data':data,
        'msg':msg if msg else status_msg.get(status)
    }