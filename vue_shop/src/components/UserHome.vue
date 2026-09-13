<template>
    <el-container>
    <el-header>
      <div>
        <img src="../assets/mi-logo.png">
        <span>电子后台管理系统</span>
      </div>
        <el-button type="primary" plain @click="logout">退出</el-button>

    </el-header>
     <el-container>
        <el-aside width="200px">
            <el-menu
            class="side-menu"
            :default-active="activeMenu"
            background-color="#001529"
            text-color="#bfcbd9"
            active-text-color="#409EFF"
            :collapse="false"
            router
            >

                <el-sub-menu
                v-for="menu in menus"
                :key="menu.id"
                :index="String(menu.id)"
                >

                <template #title>

                <el-icon>
                <component :is="menu.icon" />
                </el-icon>

                <span>{{ menu.name }}</span>

                </template>

                <el-menu-item
                v-for="child in menu.children"
                :key="child.id"
                :index="child.path"
                >

                <el-icon>
                <component :is="child.icon" />
                </el-icon>

                <span>
                {{ child.name }}
                </span>

                </el-menu-item>

                </el-sub-menu>

            </el-menu>
        </el-aside>
        <el-main>
          <router-view></router-view>
        </el-main>
     </el-container>
    </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import {
  User,
  Goods,
  Setting,
  Document,
  DataAnalysis
} from '@element-plus/icons-vue'
import { ref } from 'vue'
const router = useRouter()

const logout = () => {
  window.sessionStorage.clear()
  router.push('/login')
}

const activeMenu = ref('/user')

const menus = ref([

  {
    id: 1,
    name: '用户管理',
    icon: User,
    children: [
      {
        id: 11,
        name: '用户列表',
        path: '/user_list',
        icon: User
      }
    ]
  },

  {
    id: 2,
    name: '商品管理',
    icon: Goods,
    children: [
      {
        id: 21,
        name: '属性管理',
        path: '/product_list',
        icon: Goods
      },
      {
        id: 22,
        name: '分类列表',
        path: '/psort_list',
        icon: Goods
      },
      {
        id: 23,
        name: '商品列表',
        path: '/goods_list',
        icon: Goods
      }
    ]
  },

  {
    id: 3,
    name: '订单管理',
    icon: Document,
    children: [
      {
        id: 31,
        name: '订单列表',
        path: '/order_list',
        icon: Document
      }
    ]
  },

  {
    id: 4,
    name: '数据统计',
    icon: DataAnalysis,
    children: [
      {
        id: 41,
        name: '订单列表',
        path: '/data_list',
        icon: DataAnalysis
      }
    ]
  },

  {
    id: 5,
    name: '权限管理',
    icon: Setting,
    children: [
      {
        id: 51,
        name: '角色列表',
        path: '/author_list',
        icon: Setting
      },
      {
        id: 52,
        name: '权限列表',
        path: '/permission_list',
        icon: Setting
      }
    ]
  }

])

</script>

<style lang="less" scoped>
.home-container{
    height: 100%;
}
.el-header{
    display: flex;
    background-color: #409EFF;
    align-items: center;
    justify-content: space-between;
    color: #fff;
    font-size: 20px;
    image{
        height: 60px;
    }
    div{
        display: flex;
        align-items: center;
    }
}
.el-aside{
    background-color: rgba(0,0,0,0.2);
}
.el-main{
    background-color: #e0e0e0;
}

/* =================整个侧栏================== */
.el-aside {
  background-color: #001529;
  min-height: 100vh;
}

/* 菜单主体 */
.side-menu {
  border-right: none;
  height: 100%;
  background-color: #001529;
}

/* 一级菜单 */
.side-menu :deep(.el-sub-menu__title),
.side-menu :deep(.el-menu-item) {

  height: 50px;
  line-height: 50px;

  font-size: 14px;

  color: #bfcbd9;

}

/* 一级菜单图标 */
.side-menu :deep(.el-icon) {

  width: 20px;
  height: 20px;

  margin-right: 12px;

  font-size: 18px;

}

/* 一级菜单 hover */
.side-menu :deep(.el-sub-menu__title:hover),
.side-menu :deep(.el-menu-item:hover) {

  background-color: #263445 !important;

  color: #ffffff;

}

/* 当前激活菜单 */
.side-menu :deep(.el-menu-item.is-active) {

  color: #409EFF;

  background-color: #1d3048 !important;

}

/*
  激活菜单左侧蓝条
*/
.side-menu :deep(.el-menu-item.is-active::before) {

  content: '';

  position: absolute;

  left: 0;

  top: 10px;

  height: 30px;

  width: 3px;

  background-color: #409EFF;

}

/* 子菜单背景 */
.side-menu :deep(.el-menu) {

  background-color: #000c17;

}

/* 子菜单 */
.side-menu :deep(.el-menu-item) {

  padding-left: 50px !important;

}

/* 子菜单 hover */
.side-menu :deep(.el-menu-item:hover) {

  background-color: #1d2736 !important;

}

/* 展开箭头 */
.side-menu :deep(.el-sub-menu__icon-arrow) {

  color: #ffffff;

}

/* 菜单文字 */
.side-menu span {

  font-weight: 400;

}

/* 图标动画 */
.side-menu :deep(.el-icon) {

  transition: transform .3s;

}

.side-menu :deep(.el-menu-item:hover .el-icon),
.side-menu :deep(.el-sub-menu__title:hover .el-icon) {

  transform: scale(1.15);

}
</style>
