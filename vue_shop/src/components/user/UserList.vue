<template>

    <div class="user-list">

    <!-- 面包屑 -->

    <el-breadcrumb
      separator="/"
      class="breadcrumb"
    >

      <el-breadcrumb-item
        :to="{path:'/home'}"
      >
        首页
      </el-breadcrumb-item>

      <el-breadcrumb-item>
        用户管理
      </el-breadcrumb-item>

      <el-breadcrumb-item>
        用户列表
      </el-breadcrumb-item>

    </el-breadcrumb>

    <el-card
      shadow="hover"
      class="box-card"
    >

    <!-- 查询区域 -->

    <el-form

      :inline="true"

      :model="queryInfo"

    >

    <el-form-item

      label="用户名"

    >

    <el-input

      v-model="queryInfo.name"

      placeholder="请输入用户名"

      clearable

      @keyup.enter="getUserList"

    />

    </el-form-item>

    <el-form-item>

    <el-button

      type="primary"

      @click="getUserList"

    >

    搜索

    </el-button>

    <el-button

      @click="reset"

    >

    重置

    </el-button>

    <el-button

      type="success"

      @click="openAddDialog"

    >

    <el-icon>

      <Plus/>

    </el-icon>

    新增用户

    </el-button>

    </el-form-item>

    </el-form>

    <!-- 用户列表 -->

    <el-table

      :data="tableData"

      border

      stripe

      v-loading="loading"

      empty-text="暂无数据"

    >

    <el-table-column

      type="index"

      label="序号"

      width="70"

    />

    <el-table-column

      prop="name"

      label="姓名"

    />

    <el-table-column

      prop="nick_name"

      label="昵称"

    />

    <el-table-column

      prop="phone"

      label="电话"

    />

    <el-table-column

      prop="email"

      label="邮箱"

    />

    <el-table-column

    prop="role_name"

    label="角色名称"

    />

    <!-- 操作 -->

    <el-table-column

    label="操作"

    width="180"

    align="center"

    >

    <template #default="scope">

        <el-button

    class="table-btn"

    type="primary"

    size="small"

    @click="openEditDialog(scope.row)"

>

    <el-icon>

        <Edit />

    </el-icon>

    <span class="btn-text">
        编辑
    </span>

</el-button>

        <el-button

        class="table-btn"

        type="danger"

        size="small"

        @click="deleteUser(scope.row)"

        >

        <el-icon>

            <Delete />

        </el-icon>

        <span class="btn-text">
            删除
        </span>

        </el-button>
    </template>

    </el-table-column>

    </el-table>

    <!-- 分页 -->

    <div class="pagination">

    <el-pagination

    v-model:current-page="queryInfo.pnum"

    v-model:page-size="queryInfo.psize"

    :page-sizes="[1,2,5,10]"

    layout="total, sizes, prev, pager, next, jumper"

    :total="total"

    @size-change="handleSizeChange"

    @current-change="handleCurrentChange"

    />

    </div>

    </el-card>

    <!-- 新增用户弹窗 -->
    <el-dialog
    v-model="addDialogVisible"
    title="新增用户"
    width="500px"
    @close="addDialogClosed"
>

<el-form

    ref="addFormRef"

    :model="addForm"

    :rules="addFormRules"

    label-width="80px"

>

<el-form-item
    label="用户名"
    prop="name"
>

<el-input
    v-model="addForm.name"
/>

</el-form-item>

<el-form-item
    label="密码"
    prop="pwd"
>

<el-input

    v-model="addForm.pwd"

    type="password"

    show-password

/>

</el-form-item>

<el-form-item
    label="昵称"
>

<el-input

    v-model="addForm.nick_name"

/>

</el-form-item>

<el-form-item
    label="邮箱"
    prop="email"
>

<el-input

    v-model="addForm.email"

/>

</el-form-item>

<el-form-item
    label="电话"
    prop="phone"
>

<el-input

    v-model="addForm.phone"

/>

</el-form-item>

<el-form-item label="角色">

<el-select

    v-model="editForm.role_name"

    placeholder="请选择角色"

>

    <el-option

        v-for="r in roles"

        :key="r.id"

        :label="r.name"

        :value="r.id"

    />

</el-select>

</el-form-item>

</el-form>

<template #footer>

<el-button
@click="addDialogVisible=false"
>
取消
</el-button>

<el-button

type="primary"

@click="submitAddUser"

>
确定
</el-button>

</template>

</el-dialog>

<el-dialog

v-model="editDialogVisible"

title="编辑用户"

width="500px"

@close="editDialogClosed"

>

<el-form

ref="editFormRef"

:model="editForm"

:rules="editRules"

label-width="80px"

>

<el-form-item

label="用户名"

prop="name"

>

<el-input

v-model="editForm.name"

disabled

/>

</el-form-item>

<el-form-item

label="密码"

prop="pwd"

>

<el-input

v-model="editForm.pwd"

type="password"

show-password

placeholder="请输入新密码"

/>

</el-form-item>

<el-form-item

label="确认密码"

prop="confirmPwd"

>

<el-input

v-model="editForm.confirmPwd"

type="password"

show-password

placeholder="请再次输入密码"

/>

</el-form-item>

<el-form-item

label="邮箱"

prop="email"

>

<el-input

v-model="editForm.email"

/>

</el-form-item>

<el-form-item

label="电话"

prop="phone"

>

<el-input

v-model="editForm.phone"

/>

</el-form-item>

</el-form>

<template #footer>

<el-button

@click="editDialogVisible=false"

>

取消

</el-button>

<el-button

type="primary"

@click="submitEditUser"

>

确定

</el-button>

</template>

</el-dialog>

<el-dialog

    v-model="deleteDialogVisible"

    title="删除用户"

    width="400px"

    @close="deleteDialogClosed"

>

<div>

    确认删除用户：

    <strong>
        {{deleteUser.name}}
    </strong>

    吗？

</div>

<template #footer>

<el-button

    @click="deleteDialogVisible=false"

>

取消

</el-button>

<el-button

    type="danger"

    @click="submitDeleteUser"

>

确定删除

</el-button>

</template>

</el-dialog>

 </div>

</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

import { ElMessage } from 'element-plus'

import {
  addUserApi,
  getUserListApi,
  updateUserApi,
  deleteUserApi
} from '@/api/user'

import {
  Edit,
  Delete
} from '@element-plus/icons-vue'

import {
  getRoleListApi
} from '@/api/role'

// =====================
// 新增用户Dialog
// =====================

const addDialogVisible = ref(false)

// 表单ref

const addFormRef = ref()

// 新增用户数据

const addForm = reactive({

  name: '',

  pwd: '',

  nick_name: '',

  email: '',

  phone: ''

})

// =====================
// 邮箱验证
// =====================

const checkEmail = (rule, value, callback) => {
  const regEmail =
    /^\w+@\w+(\.\w+)+$/

  if (regEmail.test(value)) {
    callback()
  } else {
    callback(
      new Error('请输入合法的邮箱')
    )
  }
}

onMounted(() => {
  getUserList()
})

// =====================
// 手机验证
// =====================

const checkMobile = (rule, value, callback) => {
  const regMobile =
    /^1[345789]\d{9}$/

  if (regMobile.test(value)) {
    callback()
  } else {
    callback(
      new Error('请输入合法的手机号码')
    )
  }
}

// =====================
// 表单规则
// =====================

const addFormRules = {

  name: [

    {
      required: true,
      message: '请输入用户名',
      trigger: 'blur'
    },

    {
      min: 2,
      max: 10,
      message: '用户名长度2-10个字符',
      trigger: 'blur'
    }

  ],

  pwd: [

    {
      required: true,
      message: '请输入密码',
      trigger: 'blur'
    },

    {

      min: 6,

      max: 15,

      message: '密码长度6-15位',

      trigger: 'blur'

    }

  ],

  email: [

    {

      required: true,

      message: '请输入邮箱',

      trigger: 'blur'

    },

    {

      validator: checkEmail,

      trigger: 'blur'

    }

  ],

  phone: [

    {

      required: true,

      message: '请输入手机号',

      trigger: 'blur'

    },

    {

      validator: checkMobile,

      trigger: 'blur'

    }

  ]

}

function handleSizeChange (size) {
  queryInfo.psize = size

  queryInfo.pnum = 1

  getUserList()
}

function handleCurrentChange (page) {
  queryInfo.pnum = page

  getUserList()
}

// =====================
// 打开新增窗口
// =====================

function openAddDialog () {
  addDialogVisible.value = true
}

// =====================
// 关闭窗口重置
// =====================

function addDialogClosed () {
  addFormRef.value.resetFields()
}

// =====================
// 提交新增用户
// =====================

async function submitAddUser () {
  addFormRef.value.validate(
    async valid => {
      if (!valid) {
        ElMessage.error(
          '请填写完整用户信息'
        )

        return
      }

      console.log(
        '提交:',
        addForm
      )

      const res =
    await addUserApi(addForm)

      if (res.data.status !== 200) {
        ElMessage.error(
          '添加失败'
        )

        return
      }

      ElMessage.success(
        '添加成功'
      )

      addDialogVisible.value = false

      // 等弹窗关闭完成后刷新

      setTimeout(() => {
        // 回到第一页
        queryInfo.pnum = 1

        getUserList()
      }, 300)
    })
}

// =====================
// 用户列表
// =====================

const tableData = ref([])

const queryInfo = reactive({

  name: '',

  pnum: 1,

  psize: 2

})

const total = ref(0)

async function getUserList () {
  const res =
    await getUserListApi(queryInfo)

  tableData.value =
    res.data.data.users

  total.value =
    res.data.data.total
}

const editDialogVisible = ref(false)

const editFormRef = ref()

const editForm = reactive({

  id: null,

  name: '',

  pwd: '',

  confirmPwd: '',

  email: '',

  phone: '',

  role_name: null

})

const validatePwd = (rule, value, callback) => {
  if (value !== editForm.pwd) {
    callback(
      new Error(
        '两次密码输入不一致'
      )
    )
  } else {
    callback()
  }
}

const editRules = {

  name: [

    {

      required: true,

      message: '请输入用户名',

      trigger: 'blur'

    }

  ],

  pwd: [

    {

      required: true,

      message: '请输入密码',

      trigger: 'blur'

    },

    {

      min: 6,

      max: 15,

      message: '密码长度6-15位',

      trigger: 'blur'

    }

  ],

  confirmPwd: [

    {

      required: true,

      message: '请确认密码',

      trigger: 'blur'

    },

    {

      validator: validatePwd,

      trigger: 'blur'

    }

  ],

  email: [

    {

      required: true,

      message: '请输入邮箱',

      trigger: 'blur'

    }

  ],

  phone: [

    {

      required: true,

      message: '请输入电话',

      trigger: 'blur'

    }

  ]

}

function openEditDialog (row) {
  editForm.id = row.id

  editForm.name = row.name

  editForm.email = row.email

  editForm.phone = row.phone

  editForm.pwd = ''

  editForm.confirmPwd = ''

  editDialogVisible.value = true
}

function editDialogClosed () {
  editFormRef.value.resetFields()
}

async function submitEditUser () {
  editFormRef.value.validate(

    async valid => {
      if (!valid) {
        return
      }

      try {
        const res =
            await updateUserApi({

              id: editForm.id,

              pwd: editForm.pwd,

              email: editForm.email,

              phone: editForm.phone

            })

        if (res.data.status !== 200) {
          ElMessage.error(
            '修改失败'
          )

          return
        }

        ElMessage.success(
          '修改用户成功'
        )

        editDialogVisible.value = false

        getUserList()
      } catch (error) {
        console.log(error)

        ElMessage.error(
          '服务器异常'
        )
      }
    }

  )
}

// 删除弹窗

const deleteDialogVisible = ref(false)

// 保存当前删除用户

const deleteUserInfo = reactive({

  id: null,

  name: ''

})

function deleteDialogClosed () {
  deleteUserInfo.id = null

  deleteUserInfo.name = ''
}

async function submitDeleteUser () {
  try {
    const res =
    await deleteUserApi(
      {
        id: deleteUserInfo.id
      }
    )

    if (res.data.status !== 200) {
      ElMessage.error(
        '删除用户失败'
      )

      return
    }

    ElMessage.success(
      '删除用户成功'
    )

    // 关闭弹窗

    deleteDialogVisible.value = false

    // 重新加载列表

    getUserList()
  } catch (error) {
    console.log(error)

    ElMessage.error(
      '服务器异常'
    )
  }
}

// 删除用户信息
function deleteUser (row) {
  console.log('准备删除用户:', row)

  deleteUserInfo.id = row.id

  deleteUserInfo.name = row.name

  deleteDialogVisible.value = true
}

// =====================
// 角色列表
// =====================

const roles = ref([])

// =====================
// 编辑用户数据
// =====================

// =====================
// 获取角色列表
// =====================

async function getRole () {
  try {
    const res =

        await getRoleListApi()

    if (res.data.status !== 200) {
      ElMessage.error(
        res.data.msg
      )

      return
    }

    roles.value =

        res.data.data
  } catch (error) {
    console.log(error)

    ElMessage.error(
      '获取角色失败'
    )
  }
}

// 页面加载获取角色

onMounted(() => {
  getRole()
})

</script>

  <style scoped>

  .box-card{

    margin-top:20px;

  }

  .el-table{

    margin-top:20px;

  }

  .pagination{

    margin-top:20px;

    display:flex;

    justify-content:flex-end;

  }

  .table-btn {

display: inline-flex;

align-items: center;

justify-content: center;

gap: 5px;

}

.btn-text {

display: inline-flex;

align-items: center;

justify-content: center;

}

</style>
