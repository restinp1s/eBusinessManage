# vue_shop

## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Lints and fixes files
```
yarn lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

用vue3框架改写这段代码，实现相应的功能并编写order.js的api文件

2. E：Extract 数据抽取（采集）

目的：

从各种数据源获取原始数据。

常见数据来源：

数据源	方式
MySQL	SQL查询
接口API	HTTP请求
Excel	文件读取
日志	文件解析
MongoDB	数据库读取
Kafka	消息流

3. T：Transform 数据转换

原始数据通常不能直接使用，需要处理。

包括：

（1）数据清洗

删除空数据：

orders = [
x for x in orders
if x["amount"] > 0
]
（2）字段转换

例如：

订单金额：

原始：

{
"price":"299"
}

字符串：

转换：

price=int(price)

变成：

{
"price":299
}
（3）数据计算

例如：

计算订单等级：

def level(amount):


    if amount>1000:
        return "VIP"


    elif amount>500:
        return "普通"


    else:
        return "低价值"





结果：

订单	金额	等级
1001	1200	VIP
1002	300	低价值
（4）数据关联

订单：

order_id	user_id	amount
1001	1	299

用户：

user_id	name
1	张三

关联：

SELECT


o.order_id,


u.name,


o.amount




FROM orders o


JOIN user u


ON o.user_id=u.user_id;

结果：

订单	用户	金额
1001	张三	299
4. L：Load 数据加载

将处理后的数据写入目标系统。

常见：

MySQL
PostgreSQL
Hive
Elasticsearch
数据仓库

例如：

创建订单事实表：

CREATE TABLE fact_order(


order_id BIGINT,


user_id BIGINT,


amount DECIMAL(10,2),


create_time DATETIME


);

Python入库：

import pymysql




conn=pymysql.connect(
host="localhost",
user="root",
password="123456",
database="dw"
)




cursor=conn.cursor()




cursor.execute(
"""
INSERT INTO fact_order
VALUES(%s,%s,%s,NOW())
""",
(
1001,
1,
299
)
)




conn.commit()

用户列表
    |
点击编辑按钮
    |
打开编辑Dialog
    |
输入密码
输入确认密码
    |
Element Plus验证
    |
Axios PUT
    |
Flask request.get_json()
    |
修改 t_user
    |
db.session.commit()
    |
返回200
    |
提示修改成功
    |
刷新列表

ref

控制状态：

const dialogVisible=ref(false)


const roleList=ref([])
reactive

保存表单：

const roleForm=reactive({


 id:null,


 name:'',


 desc:''


})
onMounted

初始化：

onMounted(()=>{


 getRoleList()


})

简单记忆：

ref
↓
一个变量




reactive
↓
一个对象




onMounted
↓
页面加载后执行