<template>

<div class="power-menu-container">

<!-- 面包屑 -->

<el-breadcrumb separator="/">

    <el-breadcrumb-item
        :to="{path:'/home'}"
    >
        首页
    </el-breadcrumb-item>

    <el-breadcrumb-item>
        权限管理
    </el-breadcrumb-item>

    <el-breadcrumb-item>
        权限列表
    </el-breadcrumb-item>

</el-breadcrumb>

<el-card class="menu-card">

    <template #header>

        <div class="card-header">

            <span>
                权限菜单列表
            </span>

        </div>

    </template>

    <el-table

        :data="menuList"

        border

        stripe

        row-key="id"

    >

        <!-- 编号 -->

        <el-table-column

            prop="id"

            label="编号"

            width="100"

        />

        <!-- 菜单名称 -->

        <el-table-column

            label="权限名称"

        >

            <template #default="scope">

                <el-tag

                    v-if="scope.row.level===1"

                    type="primary"

                >

                    一级菜单

                </el-tag>

                <el-tag

                    v-else

                    type="success"

                >

                    二级菜单

                </el-tag>

                <span class="menu-name">

                    {{scope.row.name}}

                </span>

            </template>

        </el-table-column>

        <!-- 层级 -->

        <el-table-column

            prop="level"

            label="层级"

            width="100"

        >

            <template #default="scope">

                <el-tag

                >

                {{scope.row.level}}

                </el-tag>

            </template>

        </el-table-column>

        <!-- 父级 -->

        <el-table-column
    label="父级菜单"
    width="150"
>

<template #default="scope">

    <el-tag type="info">

        {{getParentName(scope.row.parent_id)}}

    </el-tag>

</template>

</el-table-column>

    </el-table>

</el-card>

</div>

</template>

<script setup>
import {
  ref,
  onMounted
} from 'vue'

import {
  ElMessage
} from 'element-plus'

import {
  getMenuApi
} from '@/api/menu'

// 权限列表

const menuList = ref([])

// 获取父级菜单名称
function getParentName (parentId) {
  if (parentId === 0) {
    return '顶级菜单'
  }

  const parent = menuList.value.find(
    item => item.id === parentId
  )

  return parent
    ? parent.name
    : '-'
}

// 获取菜单

async function getMenuList () {
  const res =
    await getMenuApi({
      type: 'list'
    })

  if (res.data.status !== 200) {
    ElMessage.error(
      res.data.msg
    )

    return
  }

  menuList.value =
    res.data.data
}

onMounted(() => {
  getMenuList()
})

</script>

<style scoped>
.power-menu-container{

width:100%;

}

.el-breadcrumb{

margin-bottom:20px;

}

.menu-card{

margin-top:20px;

}

.card-header{

font-size:18px;

font-weight:bold;

}

.menu-name{

margin-left:15px;

}

</style>
