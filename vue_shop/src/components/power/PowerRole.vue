<template>

    <div class="role-container">

        <!-- 面包屑 -->

        <el-breadcrumb separator="/">

            <el-breadcrumb-item :to="{path:'/home'}">
                首页
            </el-breadcrumb-item>

            <el-breadcrumb-item>
                权限管理
            </el-breadcrumb-item>

            <el-breadcrumb-item>
                角色列表
            </el-breadcrumb-item>

        </el-breadcrumb>

        <el-card class="role-card">

            <!-- 新增按钮 -->

            <el-button
                type="primary"
                @click="openAddDialog"
            >

                新增角色

            </el-button>

            <!-- 角色列表 -->

            <el-table
                :data="roleList"
                border
                style="margin-top:20px"
            >

            <el-table-column type="expand">

              <template #default="scope">

                <el-row
                  v-for="(m,i) in scope.row.menu"
                  :key="m.id"
                  :class="[
                    'bottom',
                    i===0?'top':'',
                    'rcenter'
                  ]"
                >

                  <!-- 一级菜单 -->
                  <el-col :span="10">

                    <el-tag
                      closable
                      @close="removeMenu(scope.row,m)"
                    >
                      {{ m.name }}
                    </el-tag>

                    <el-icon>
                      <CaretRight />
                    </el-icon>

                  </el-col>

                  <!-- 二级菜单 -->

                  <el-col :span="14">

                    <el-tag

                      v-for="sm in m.children"

                      :key="sm.id"

                      type="success"

                      closable

                      @close="removeMenu(scope.row,sm)"

                    >

                      {{ sm.name }}

                    </el-tag>

                  </el-col>

                </el-row>

              </template>

            </el-table-column>

                <el-table-column
                    prop="id"
                    label="ID"
                    width="80"
                />

                <el-table-column
                    prop="name"
                    label="角色名称"
                />

                <el-table-column
                    prop="desc"
                    label="角色详情"
                />

                <el-table-column
                    label="操作"
                    width="220"
                >

                <template #default="scope">

                    <el-button

                        type="primary"

                        size="small"

                        @click="openEditDialog(scope.row)"

                    >

                        修改

                    </el-button>

                    <el-button

                        type="danger"

                        size="small"

                        @click="deleteRole(scope.row)"

                    >

                        删除

                    </el-button>

                    <el-button

                        type="warning"

                        size="small"

                        @click="showMenuDialog(scope.row)"

                    >

                        分配

                    </el-button>

                </template>

                </el-table-column>

            </el-table>

        </el-card>

    <!-- 新增/修改角色 -->
    <el-dialog

v-model="roleDialogVisible"

:title="dialogTitle"

width="400px"

>

<el-form

ref="roleFormRef"

:model="roleForm"

:rules="roleRules"

label-width="80px"

>

<el-form-item

label="角色名称"

prop="name"

>

<el-input

v-model="roleForm.name"

/>

</el-form-item>

<el-form-item

label="角色描述"

prop="desc"

>

<el-input

v-model="roleForm.desc"

/>

</el-form-item>

</el-form>

<template #footer>

<el-button

@click="roleDialogVisible=false"

>

取消

</el-button>

<el-button

type="primary"

@click="submitRole"

>

确定

</el-button>

</template>

</el-dialog>

        <!-- 权限分配弹窗 -->

        <el-dialog

            v-model="menuDialogVisible"

            title="分配权限"

            width="500px"

            @close="handleClose"

        >

            <el-tree

                ref="treeRef"

                :data="menuList"

                :props="menuProps"

                node-key="id"

                show-checkbox

                default-expand-all

                :default-checked-keys="keyList"

            />

            <template #footer>

                <el-button

                    @click="handleClose"

                >

                    取消

                </el-button>

                <el-button

                    type="primary"

                    @click="editRM()"

                >

                    确定

                </el-button>

            </template>

        </el-dialog>

    </div>

    </template>

<script setup>

import {
  ref,
  reactive,
  onMounted
} from 'vue'

import {
  ElMessage,
  ElMessageBox
} from 'element-plus'

import {
  getRoleListApi,
  addRoleApi,
  updateRoleApi,
  deleteRoleApi

} from '@/api/role'

import {
  CaretRight
} from '@element-plus/icons-vue'

import {
  deleteMenuApi,
  getMenuApi,
  setRoleMenuApi
} from '@/api/menu'

// =======================
// 角色列表
// =======================

const roleList = ref([])

async function getRoleList () {
  const res =
  await getRoleListApi()

  if (res.data.status !== 200) {
    ElMessage.error(
      res.data.msg
    )

    return
  }

  roleList.value =
  res.data.data
}

onMounted(() => {
  getRoleList()
})

// =======================
// 角色新增/修改弹窗
// =======================

const roleDialogVisible =
ref(false)

const dialogTitle =
ref('新增角色')

const roleFormRef =
ref()

const roleForm =
reactive({

  id: null,

  name: '',

  desc: ''

})

// =======================
// 表单验证
// =======================

const roleRules = {

  name: [

    {

      required: true,

      message: '请输入角色名称',

      trigger: 'blur'

    },

    {

      min: 2,

      max: 10,

      message: '长度2-10字符',

      trigger: 'blur'

    }

  ],

  desc: [

    {

      required: true,

      message: '请输入角色描述',

      trigger: 'blur'

    }

  ]

}

// =======================
// 新增角色
// =======================

function openAddDialog () {
  dialogTitle.value =
  '新增角色'

  roleForm.id = null

  roleForm.name = ''

  roleForm.desc = ''

  roleDialogVisible.value = true
}

// =======================
// 修改角色
// =======================

function openEditDialog (row) {
  dialogTitle.value =
  '修改角色'

  roleForm.id =
  row.id

  roleForm.name =
  row.name

  roleForm.desc =
  row.desc

  roleDialogVisible.value = true
}

// =======================
// 保存角色
// =======================

async function submitRole () {
  const valid =
  await roleFormRef.value.validate()

  if (!valid) {
    return
  }

  let res

  if (roleForm.id) {
    res =
    await updateRoleApi(
      roleForm
    )
  } else {
    res =
    await addRoleApi(
      roleForm
    )
  }

  if (res.data.status !== 200) {
    ElMessage.error(
      res.data.msg
    )

    return
  }

  ElMessage.success(
    '操作成功'
  )

  roleDialogVisible.value = false

  getRoleList()
}

// =======================
// 删除角色
// =======================

async function deleteRole (row) {
  try {
    await ElMessageBox.confirm(

      `确认删除角色${row.name}吗?`,

      '提示',

      {

        type: 'warning',

        confirmButtonText: '确定',

        cancelButtonText: '取消'

      }

    )

    const res =
    await deleteRoleApi({

      id: row.id

    })

    if (res.data.status !== 200) {
      ElMessage.error(
        res.data.msg
      )

      return
    }

    ElMessage.success(
      '删除成功'
    )

    getRoleList()
  } catch {
    ElMessage.info(
      '取消删除'
    )
  }
}

// =================================================
// 权限分配
// =================================================

const menuDialogVisible =
ref(false)

// 权限树

const menuList =
ref([])

const menuProps = {

  label: 'name',

  children: 'children'

}

// tree实例

const treeRef =
ref()

// 当前角色id

const roleId =
ref(null)

// 已选权限

const keyList =
ref([])

// =======================
// 打开权限弹窗
// =======================

async function showMenuDialog (row) {
  menuDialogVisible.value = true

  roleId.value =
  row.id

  keyList.value = []

  const res =
  await getMenuApi()

  if (res.data.status !== 200) {
    ElMessage.error(
      res.data.msg
    )

    return
  }

  menuList.value =
  res.data.data

  getKeys(
    row.menu
  )
}

// =======================
// 默认勾选权限
// =======================

function getKeys (menu) {
  keyList.value = []

  menu.forEach(item => {
    if (
      item.children &&
      item.children.length
    ) {
      item.children.forEach(child => {
        keyList.value.push(
          child.id
        )
      })
    } else {
      keyList.value.push(
        item.id
      )
    }
  })
}

// =======================
// 保存权限
// =======================

async function editRM () {
  const checked =
  treeRef.value.getCheckedKeys()

  const half =
  treeRef.value.getHalfCheckedKeys()

  const mids = [
    ...half,
    ...checked
  ]

  const res =
  await setRoleMenuApi({

    rid: roleId.value,

    mids: mids.join(',')

  })

  if (res.data.status !== 200) {
    ElMessage.error(
      res.data.msg
    )

    return
  }

  ElMessage.success(
    '权限修改成功'
  )

  function handleClose () {
    menuDialogVisible.value = false

    roleId.value = null

    keyList.value = []

    menuList.value = []
  }

  // 关闭权限弹窗
  menuDialogVisible.value = false

  // 清理数据
  handleClose()

  getRoleList()
}

// =======================
// 删除角色权限
// =======================

async function removeMenu (role, targetMenu) {
  try {
    await ElMessageBox.confirm(

      `确认删除权限【${targetMenu.name}】吗？`,

      '提示',

      {

        type: 'warning',

        confirmButtonText: '确定',

        cancelButtonText: '取消'

      }

    )

    const res =
    await deleteMenuApi({

      rid: role.id,

      mid: targetMenu.id

    })

    if (res.data.status !== 200) {
      ElMessage.error(
        res.data.msg
      )

      return
    }

    // 删除前端数据

    role.menu =
    role.menu.filter(

      item =>
        item.id !== targetMenu.id

    )

    role.menu.forEach(parent => {
      if (parent.children) {
        parent.children =
        parent.children.filter(

          item =>
            item.id !== targetMenu.id

        )
      }
    })

    ElMessage.success(
      '删除权限成功'
    )
  } catch {
    ElMessage.info(
      '取消删除'
    )
  }
}

</script>

<style lang="less" scoped>
  .top{
    border-top: 1px solid #eee;
  }
  .bottom{
    border-bottom: 1px solid #eee;
  }
  .el_tag{
    margin: 10px;
  }
  .rcenter{
    display: flex;
    align-items: center;
  }
  .role-container{

width:100%;

}

.el-breadcrumb{

margin-bottom:20px;

}

.role-card{

margin-top:10px;

}
</style>
