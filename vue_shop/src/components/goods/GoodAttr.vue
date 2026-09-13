<template>

    <div>

    <el-breadcrumb separator="/" class="topBread">

    <el-breadcrumb-item>
    首页
    </el-breadcrumb-item>

    <el-breadcrumb-item>
    商品管理
    </el-breadcrumb-item>

    <el-breadcrumb-item>
    分类参数
    </el-breadcrumb-item>

    </el-breadcrumb>

    <el-card>

    <el-alert
    title="注意：只有三级分类可以设置参数"
    type="warning"
    />

    <!-- 分类选择 -->

    <div class="cate-select">

    <span>
    选择商品分类：
    </span>

    <el-cascader

    v-model="selectKeys"

    :options="cateList"

    :props="cateProps"

    clearable

    @change="changeSelector"

    />

    </div>

    <el-tabs
    v-model="activeName"
    @tab-change="handleTabChange"
    >

    <!-- 静态参数 -->

    <el-tab-pane
    label="静态参数"
    name="static"
    >

    <el-button

    type="primary"

    :disabled="btnDisabled"

    @click="openDialog"

    >

    增加参数

    </el-button>

    <el-table
    :data="staticAttr"
    border
    style="width:100%"
    >

    <el-table-column
    type="expand"
    >

    <template #default="{row}">

    <el-tag>
    {{row.val}}
    </el-tag>

    </template>

    </el-table-column>

    <el-table-column
    type="index"
    />

    <el-table-column

    label="参数名称"

    prop="name"

    />

            <el-table-column
        label="操作"
        width="180"
        >
        <template #default="{row}">

            <el-button
            type="primary"
            size="small"
            @click="editAttr(row)"
            >
            编辑
            </el-button>

            <el-button
            type="danger"
            size="small"
            @click="deleteAttr(row)"
            >
            删除
            </el-button>

        </template>
    </el-table-column>

    </el-table>

    </el-tab-pane>

    <!-- 动态参数 -->

    <el-tab-pane

    label="动态参数"

    name="dynamic"

    >

    <el-button

    type="primary"

    :disabled="btnDisabled"

    @click="openDialog"

    >

    增加参数

    </el-button>

    <el-table

    :data="dynamicAttr"

    border

    style="width:100%"

    >

    <el-table-column

    type="expand"

    >

    <template #default="{row}">

    <el-tag

    v-for="(item,index) in row.val"

    :key="index"

    closable

    @click="removeTag(row,index)"

    >

    {{item}}

    </el-tag>

    <el-input

    v-if="row.inputVisible"

    v-model="row.inputValue"

    class="input-tag"

    @keyup.enter="confirmTag(row)"

    @blur="confirmTag(row)"

    />

    <el-button

    v-else

    size="small"

    @click="showInput(row)"

    >

    {{ '+ New Tag' }}

    </el-button>

    </template>

    </el-table-column>

    <el-table-column
    type="index"
    />

    <el-table-column

    label="参数名称"

    prop="name"

    />

        <el-table-column
        label="操作"
        width="180"
        >
        <template #default="{row}">

            <el-button
            type="primary"
            size="small"
            @click="editAttr(row)"
            >
            编辑
            </el-button>

            <el-button
            type="danger"
            size="small"
            @click="deleteAttr(row)"
            >
            删除
            </el-button>

        </template>
    </el-table-column>

    </el-table>

    </el-tab-pane>

    </el-tabs>

    </el-card>

    <!-- 新增弹窗 -->

    <el-dialog

    v-model="dialogVisible"

    :title="'添加'+titleText"

    width="30%"

    >

    <el-form

    :model="form"

    ref="formRef"

    >

    <el-form-item

    :label="titleText"

    >

    <el-input

    v-model="form.name"

    />

    </el-form-item>

    <el-button

    type="primary"

    @click="addAttr"

    >

    确定

    </el-button>

    </el-form>

    </el-dialog>

    </div>

    </template>

<script setup>

import {
  ref,
  computed,
  onMounted
} from 'vue'

import {
  ElMessage,
  ElMessageBox
} from 'element-plus'

import {

  getCategoryListApi,

  getAttributeListApi,

  addAttributeApi,

  updateAttributeApi,

  deleteAttributeApi,

  getAttributeDetailApi

} from '@/api/attribute'

// 分类

const cateList = ref([])

const selectKeys = ref([])

const cateProps = {

  label: 'name',

  value: 'id',

  children: 'children',

  emitPath: true

}

// 当前tab

const activeName = ref('static')

// 参数

const staticAttr = ref([])

const dynamicAttr = ref([])

// 弹窗

const dialogVisible = ref(false)

const form = ref({
  id: null,

  name: ''

})

const editMode = ref(false)

// 当前分类id

const cid = computed(() => {
  return selectKeys.value[2]
})

const btnDisabled = computed(() => {
  return selectKeys.value.length !== 3
})

const titleText = computed(() => {
  return activeName.value === 'static'
    ? '静态参数'
    : '动态参数'
})

// 获取分类

async function getCateList () {
  try {
    const res = await getCategoryListApi()

    console.log('接口完整返回:', res)

    console.log(
      '后端数据:',
      res.data
    )

    if (res.data.status !== 200) {
      ElMessage.error(res.data.msg)

      return
    }

    const list = res.data.data.data

    console.log(
      '分类数组:',
      list
    )

    if (Array.isArray(list)) {
      cateList.value = list
    } else {
      cateList.value = []

      ElMessage.error(
        '分类数据格式错误'
      )
    }
  } catch (error) {
    console.error(
      '分类请求失败',
      error
    )

    ElMessage.error(
      '获取分类失败'
    )
  }
}

// 分类变化

function changeSelector () {
  console.log(
    '选择结果:',
    selectKeys.value
  )

  if (selectKeys.value.length !== 3) {
    staticAttr.value = []

    dynamicAttr.value = []

    return
  }

  getAttribute()
}

// tab切换

function handleTabChange () {
  if (cid.value) {
    getAttribute()
  }
}

// 获取属性

async function getAttribute () {
  console.log('进入 getAttribute')

  console.log('cid:', cid.value)

  console.log('type:', activeName.value)

  const res =
    await getAttributeListApi({

      cid: cid.value,

      _type: activeName.value

    })

  if (res.data.status !== 200) {
    return ElMessage.error(res.data.msg)
  }

  if (activeName.value === 'static') {
    staticAttr.value = res.data.data
  } else {
    dynamicAttr.value =
    res.data.data.map(item => ({

      ...item,

      val: item.val
        ? item.val.split(',')
        : [],

      inputVisible: false,

      inputValue: ''

    }))
  }
}

// 打开新增

function openDialog () {
  editMode.value = false

  form.value = {
    id: null,
    name: ''
  }

  dialogVisible.value = true
}

// 新增

async function addAttr () {
  let res

  // 编辑
  if (editMode.value) {
    res =
  await updateAttributeApi({

    id: form.value.id,

    cid: cid.value,

    _type: activeName.value,

    name: form.value.name

  })
  } else {
    res =
  await addAttributeApi({

    cid: cid.value,

    _type: activeName.value,

    name: form.value.name

  })
  }

  if (res.data.status !== 200) {
    return ElMessage.error(
      res.data.msg
    )
  }

  ElMessage.success(
    res.data.msg
  )

  dialogVisible.value = false

  form.value = {
    id: null,
    name: ''
  }

  editMode.value = false

  getAttribute()
}

// 显示输入框

async function showInput (row) {
  const res =
  await getAttributeDetailApi(row.id)

  if (res.data.status !== 200) {
    ElMessage.error(
      res.data.msg
    )

    return
  }

  row.val =
  res.data.data.val
    ? res.data.data.val.split(',')
    : []

  row.inputVisible = true
}

// 添加tag

function confirmTag (row) {
  if (!row.inputValue.trim()) {
    row.inputVisible = false

    return
  }

  row.val.push(
    row.inputValue
  )

  row.inputValue = ''

  row.inputVisible = false

  saveAttribute(row)
}

// 删除tag

function removeTag (row, index) {
  row.val.splice(index, 1)

  saveAttribute(row)
}

// 保存动态参数

async function saveAttribute (row) {
  const res =
    await updateAttributeApi({

      id: row.id,

      name: row.name,

      cid: row.cid,

      val: row.val.join(',')

    })

  if (res.data.status === 200) {
    ElMessage.success('保存成功')
  }
}

onMounted(() => {
  getCateList()
})

function editAttr (row) {
  editMode.value = true

  form.value = {

    id: row.id,

    name: row.name

  }

  dialogVisible.value = true
}

async function deleteAttr (row) {
  try {
    await ElMessageBox.confirm(

      '确认删除该参数吗？',

      '提示',

      {
        type: 'warning'
      }

    )

    const res =
        await deleteAttributeApi(row.id)

    if (res.data.status !== 200) {
      return ElMessage.error(
        res.data.msg
      )
    }

    ElMessage.success(
      '删除成功'
    )

    getAttribute()
  } catch (e) {

  }
}
</script>

    <style scoped>

    .cate-select{

    margin:20px 0;

    }

    .el-tag{

    margin:5px;

    }

    .input-tag{

    width:120px;

    }

    .topBread {
  display: flexbox;
  margin-top: 0px;
  margin-bottom: 15px;
    }

</style>
