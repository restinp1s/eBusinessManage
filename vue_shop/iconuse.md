1. 用户类 User
User
Avatar
UserFilled
UserSolid
Postcard

示例：

<el-icon>
  <User />
</el-icon>
2. 登录 / 权限 / 安全类
Lock
Unlock
Key
View
Hide
CircleClose
Warning
WarningFilled

常用于：

登录
密码
权限管理

例如：

import { Lock } from '@element-plus/icons-vue'
3. 文件类
Document
DocumentAdd
DocumentChecked
DocumentCopy
DocumentDelete
DocumentRemove
Folder
FolderAdd
FolderChecked
FolderDelete
FolderOpened
Files
Tickets
Notebook
Collection
4. 操作类（后台系统最常用）
Plus
Minus
Close
Check
Delete
Edit
EditPen
Search
Refresh
Download
Upload
Share
CopyDocument
Finished
CirclePlus
CircleMinus

例如：

删除按钮：

<el-icon>
    <Delete/>
</el-icon>
5. 箭头方向类
ArrowLeft
ArrowRight
ArrowUp
ArrowDown

ArrowLeftBold
ArrowRightBold
ArrowUpBold
ArrowDownBold

DArrowLeft
DArrowRight

CaretLeft
CaretRight
CaretTop
CaretBottom
6. 菜单导航类
Menu
Grid
HomeFilled
House
Location
Position
Compass
Guide
Setting
Tools
Operation

后台管理系统常用：

Menu
Setting
HomeFilled
7. 时间日期类
Clock
Timer
Calendar
Date
AlarmClock
Watch
8. 数据统计类
DataLine
DataAnalysis
TrendCharts
Histogram
PieChart
Management
Monitor
Odometer

适合：

数据大屏
仪表盘
9. 网络通信类
Connection
Link
LinkBroken
Share
Promotion
Position
Message
ChatDotRound
ChatLineRound
10. 图片 / 媒体类
Picture
PictureFilled
PictureRounded
Camera
VideoCamera
Film
Microphone
Headset
11. 电商常用
ShoppingCart
Goods
GoodsFilled
ShoppingBag
Present
Wallet
Money
PriceTag
Discount
Sell
SoldOut

例如：

购物车：

import { ShoppingCart } from '@element-plus/icons-vue'
12. 状态类

成功：

SuccessFilled
CircleCheck
CircleCheckFilled
Check

失败：

CircleClose
CircleCloseFilled
CloseBold

提示：

InfoFilled
QuestionFilled
WarningFilled
13. 设备类
Phone
Iphone
Monitor
Printer
Cpu
Laptop
Connection
ChromeFilled
Eleme
ElemeFilled
14. 文件上传下载
Upload
UploadFilled
Download
FolderOpened
Files
DocumentAdd
15. 常用后台管理菜单组合

一个商城后台通常：

import {
    House,
    User,
    Goods,
    ShoppingCart,
    DataAnalysis,
    Setting,
    Document,
    Search
} from '@element-plus/icons-vue'

对应：

首页        House
用户管理    User
商品管理    Goods
订单管理    ShoppingCart
数据统计    DataAnalysis
系统设置    Setting
日志管理    Document
搜索        Search