<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator="/" class="topBread">
      <el-breadcrumb-item :to="{ path: '/home' }">
        首页
      </el-breadcrumb-item>

      <el-breadcrumb-item>
        商品管理
      </el-breadcrumb-item>

      <el-breadcrumb-item>
        商品分类
      </el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 内容 -->
    <el-card class="role-card">
      <!-- 新增按钮 -->
      <el-row>
        <el-button
          type="primary"
          @click="showAddCateDialog"
        >
          新增分类
        </el-button>
      </el-row>

      <!-- 分类树 -->
      <el-row class="table-row">
        <el-table
          :data="cateList"
          row-key="id"
          border
          class="tree-table"
        >
          <!-- 序号 -->
          <el-table-column
            type="index"
            label="#"
            width="60"
            align="center"
          />

          <!-- 分类名称 -->
          <el-table-column
            prop="name"
            label="分类名称"
            min-width="250"
          />

          <!-- 分类级别 -->
          <el-table-column
            prop="level"
            label="分类级别"
            width="120"
            align="center"
          >
            <template #default="scope">
              <el-tag v-if="scope.row.level === 1">
                一级分类
              </el-tag>

              <el-tag
                v-else-if="scope.row.level === 2"
                type="success"
              >
                二级分类
              </el-tag>

              <el-tag
                v-else-if="scope.row.level === 3"
                type="warning"
              >
                三级分类
              </el-tag>
            </template>
          </el-table-column>

          <!-- 操作 -->
          <el-table-column
            label="操作"
            width="180"
            align="center"
          >
            <template #default="scope">
              <el-button
                size="small"
                type="primary"
                @click="handleEdit(scope.row)"
              >
                编辑
              </el-button>

              <el-button
                size="small"
                type="danger"
                @click="handleDelete(scope.row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </el-card>

    <!-- 新增分类弹窗 -->
    <el-dialog
      v-model="addCateDialogVisible"
      title="增加分类"
      width="30%"
      @close="closeCateDialog"
    >
      <el-form
        ref="addCateRef"
        :model="addCateForm"
        :rules="addCateRules"
        label-width="80px"
      >
        <!-- 分类名称 -->
        <el-form-item
          label="分类名称"
          prop="name"
        >
          <el-input
            v-model="addCateForm.name"
            placeholder="请输入分类名称"
          />
        </el-form-item>

        <!-- 父类节点 -->
        <el-form-item label="父类节点">
          <el-cascader
            v-model="selectKeys"
            :options="catePidlist"
            :props="cascaderProps"
            clearable
            separator=" > "
            @change="changeSelector"
          />
        </el-form-item>

        <!-- 按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            @click="addCate"
          >
            确定
          </el-button>

          <el-button @click="closeCateDialog">
            取消
          </el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

import {
  getCategoryListApi,
  addCategoryApi,
  deleteCategoryApi
} from '@/api/category'

// =========================
// 分类列表
// =========================

const cateList = ref([])

// =========================
// 新增分类弹窗
// =========================

const addCateDialogVisible = ref(false)

// 表单 DOM
const addCateRef = ref(null)

// 新增分类表单
const addCateForm = ref({
  name: '',
  pid: 0,
  level: 1
})

// 表单验证规则
const addCateRules = {
  name: [
    {
      required: true,
      message: '请输入分类名称',
      trigger: 'blur'
    }
  ]
}

// =========================
// 父级分类
// =========================

const catePidlist = ref([])

// Cascader 当前选择值
const selectKeys = ref([])

// Cascader 配置
const cascaderProps = {
  expandTrigger: 'hover',
  label: 'name',
  value: 'id',
  checkStrictly: true
}

// =========================
// 获取分类列表
// =========================

async function getCategoryList () {
  try {
    const res = await getCategoryListApi()

    console.log('完整响应：', res)
    console.log('res.data：', res.data)
    console.log('res.data.data：', res.data.data)
    console.log('res.data.data.data：', res.data.data.data)

    // 后端实际结构：
    //
    // {
    //   status: 200,
    //   msg: '获取商品分类列表成功！',
    //   data: {
    //     data: [...]
    //   }
    // }
    //
    // 所以真正的数组是：
    // res.data.data.data

    if (res.data.status !== 200) {
      ElMessage.error(
        res.data.msg || '获取商品分类失败'
      )
      return
    }

    const list = res.data.data.data

    console.log(
      '分类列表是否数组：',
      Array.isArray(list)
    )

    if (!Array.isArray(list)) {
      console.error(
        '分类数据格式错误：',
        list
      )

      cateList.value = []

      ElMessage.error('分类数据格式错误')

      return
    }

    cateList.value = list

    console.log(
      '最终 cateList：',
      cateList.value
    )
  } catch (error) {
    console.error(
      '获取分类列表失败：',
      error
    )

    cateList.value = []

    ElMessage.error('获取分类列表失败')
  }
}

// =========================
// 打开新增分类弹窗
// =========================

async function showAddCateDialog () {
  await getCatePidList()

  addCateDialogVisible.value = true
}

// =========================
// 获取父级分类
// =========================

async function getCatePidList () {
  try {
    const res = await getCategoryListApi({
      level: 2
    })

    console.log(
      '父级分类接口返回：',
      res
    )

    if (res.data.status !== 200) {
      ElMessage.error(
        res.data.msg || '获取父级分类失败'
      )

      return
    }

    const list = res.data.data.data

    console.log(
      '父级分类列表：',
      list
    )

    if (!Array.isArray(list)) {
      console.error(
        '父级分类不是数组：',
        list
      )

      catePidlist.value = []

      ElMessage.error('父级分类数据格式错误')

      return
    }

    catePidlist.value = list
  } catch (error) {
    console.error(
      '获取父级分类失败：',
      error
    )

    catePidlist.value = []

    ElMessage.error('获取父级分类失败')
  }
}

// =========================
// Cascader 选择
// =========================

function changeSelector (value) {
  console.log(
    '当前选择的分类：',
    value
  )

  if (value && value.length > 0) {
    // 最后一级就是父分类 ID
    addCateForm.value.pid =
      value[value.length - 1]

    // 选择一级 -> 新增二级
    // 选择二级 -> 新增三级
    addCateForm.value.level =
      value.length + 1
  } else {
    // 没有选择父节点
    // 新增一级分类
    addCateForm.value.pid = 0

    addCateForm.value.level = 1
  }

  console.log(
    '当前新增分类参数：',
    addCateForm.value
  )
}

// =========================
// 新增分类
// =========================

async function addCate () {
  try {
    // 表单验证
    await addCateRef.value.validate()

    console.log(
      '准备新增分类：',
      addCateForm.value
    )

    const res = await addCategoryApi(
      addCateForm.value
    )

    console.log(
      '新增分类接口返回：',
      res
    )

    if (res.data.status !== 200) {
      ElMessage.error(
        res.data.msg || '新增分类失败'
      )

      return
    }

    ElMessage.success(
      res.data.msg || '新增分类成功'
    )

    // 重新获取分类树
    await getCategoryList()

    // 关闭弹窗
    closeCateDialog()
  } catch (error) {
    console.error(
      '新增分类失败：',
      error
    )
  }
}

// =========================
// 编辑
// =========================

function handleEdit (row) {
  console.log(
    '当前编辑分类：',
    row
  )

  ElMessage.info(
    `编辑：${row.name}`
  )
}

// =========================
// 删除
// =========================

async function handleDelete (row) {
  try {
    await ElMessageBox.confirm(
      `确定要删除分类「${row.name}」吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const res = await deleteCategoryApi(
      row.id
    )

    console.log(
      '删除接口返回：',
      res.data
    )

    if (res.data.status !== 200) {
      ElMessage.error(
        res.data.msg || '删除失败'
      )

      return
    }

    ElMessage.success(
      res.data.msg || '删除成功'
    )

    // 重新加载分类
    await getCategoryList()
  } catch (error) {
    // Element Plus 取消确认时通常返回 'cancel'
    if (error === 'cancel') {
      return
    }

    console.error(
      '删除分类失败：',
      error
    )

    ElMessage.error('删除失败')
  }
}

// =========================
// 关闭弹窗
// =========================

function closeCateDialog () {
  // 重置表单
  if (addCateRef.value) {
    addCateRef.value.resetFields()
  }

  // 重置 Cascader
  selectKeys.value = []

  // 重置新增参数
  addCateForm.value = {
    name: '',
    pid: 0,
    level: 1
  }

  addCateDialogVisible.value = false
}

// =========================
// 页面加载
// =========================

onMounted(() => {
  getCategoryList()
})
</script>

<style scoped>
.tree-table {
  margin-top: 15px;
}

.table-row {
  margin-top: 15px;
}

.topBread {
  display: flexbox;
  margin-top: 0px;
  margin-bottom: 15px;
}

</style>
