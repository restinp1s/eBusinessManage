<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">
        首页
      </el-breadcrumb-item>

      <el-breadcrumb-item>
        商品管理
      </el-breadcrumb-item>

      <el-breadcrumb-item>
        增加商品
      </el-breadcrumb-item>
    </el-breadcrumb>

    <el-card>
      <el-alert
        title="增加商品信息"
        type="info"
        center
        show-icon
      />

      <!-- 步骤条 -->
      <el-steps
        :active="Number(active)"
        finish-status="success"
        align-center
      >
        <el-step title="基本信息" />
        <el-step title="商品静态参数" />
        <el-step title="商品动态参数" />
        <el-step title="商品图片" />
        <el-step title="商品内容" />
        <el-step title="完成" />
      </el-steps>

      <el-form
        ref="addRef"
        :model="addForm"
        :rules="addRules"
        label-position="top"
        @submit.prevent
      >
        <el-tabs
          v-model="active"
          tab-position="left"
          @tab-change="handleTabChange"
        >
          <!-- ================= 基本信息 ================= -->
          <el-tab-pane
            label="基本信息"
            name="0"
          >
            <el-form-item
              label="商品名称"
              prop="name"
            >
              <el-input
                v-model="addForm.name"
                placeholder="请输入商品名称"
              />
            </el-form-item>

            <el-form-item
              label="商品价格"
              prop="price"
            >
              <el-input
                v-model="addForm.price"
                placeholder="请输入商品价格"
              />
            </el-form-item>

            <el-form-item
              label="商品数量"
              prop="number"
            >
              <el-input
                v-model="addForm.number"
                placeholder="请输入商品数量"
              />
            </el-form-item>

            <el-form-item
              label="商品权重"
              prop="weight"
            >
              <el-input
                v-model="addForm.weight"
                placeholder="请输入商品权重"
              />
            </el-form-item>

            <el-form-item
              label="商品分类"
              prop="cid"
            >
              <el-cascader
                v-model="selectKeys"
                :options="cateIdList"
                :props="{
                  expandTrigger: 'hover',
                  label: 'name',
                  value: 'id'
                }"
                clearable
                separator=" > "
                @change="changeSelector"
              />
            </el-form-item>
          </el-tab-pane>

          <!-- ================= 静态参数 ================= -->
          <el-tab-pane
            label="商品静态参数"
            name="1"
          >
            <el-form-item
              v-for="item in attrStatic"
              :key="item.id"
              :label="item.name"
            >
              <el-input v-model="item.val" />
            </el-form-item>
          </el-tab-pane>

          <!-- ================= 动态参数 ================= -->
          <el-tab-pane
            label="商品动态参数"
            name="2"
            >
            <el-form-item
                v-for="item in attrDynamic"
                :key="item.id"
                :label="item.name"
            >
                <el-checkbox-group v-model="item.selected">
                <el-checkbox
                    v-for="(option, index) in item.options"
                    :key="index"
                    :label="option"
                    border
                >
                    {{ option }}
                </el-checkbox>
                </el-checkbox-group>
            </el-form-item>
            </el-tab-pane>

          <!-- ================= 商品图片 ================= -->
          <el-tab-pane
            label="商品图片"
            name="3"
          >
            <el-upload
              class="upload-demo"
              action="/upload_img"
              list-type="picture"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :on-success="handleSuccess"
            >
              <el-button
                size="small"
                type="primary"
              >
                点击上传
              </el-button>
            </el-upload>
          </el-tab-pane>

          <!-- ================= 商品内容 ================= -->
            <el-tab-pane
            label="商品内容"
            name="4"
            >
            <div class="editor-wrapper">
                <QuillEditor
                v-model:content="addForm.introduce"
                content-type="html"
                theme="snow"
                :toolbar="[
                    ['bold', 'italic', 'underline', 'strike'],
                    ['blockquote', 'code-block'],
                    [{ header: 1 }, { header: 2 }],
                    [{ list: 'ordered' }, { list: 'bullet' }],
                    [{ indent: '-1' }, { indent: '+1' }],
                    [{ size: ['small', false, 'large', 'huge'] }],
                    [{ color: [] }, { background: [] }],
                    [{ align: [] }],
                    ['link', 'image'],
                    ['clean']
                ]"
                style="height: 400px"
                />
            </div>

            <el-button
                type="primary"
                class="btn-add"
                @click="goodsAdd"
                native-type="button"
            >
                添加商品
            </el-button>
            </el-tab-pane>

        </el-tabs>

        </el-form>
    </el-card>
    <!-- 图片预览 -->
    <el-dialog
      v-model="previewVisible"
      title="图片预览"
      width="40%"
    >
      <img
        :src="previewPath"
        class="pre-img"
      />
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
  ElMessage
} from 'element-plus'

import {
  getCategoryListApi,
  getAttributeListApi
} from '@/api/category'

import { QuillEditor } from '@vueup/vue-quill'

import '@vueup/vue-quill/dist/vue-quill.snow.css'

import axios from 'axios'

// ===============================
// 表单 Ref
// ===============================

const addRef = ref(null)

// ===============================
// 当前步骤
// ===============================

const active = ref('0')

// ===============================
// 商品表单
// ===============================

const addForm = reactive({
  name: '',
  price: 0,
  number: 0,
  weight: 0,

  cid_one: 0,
  cid_two: 0,
  cid_three: 0,

  pics: [],

  introduce: '',

  attr_static: [],
  attr_dynamic: []
})

// ===============================
// 表单验证
// ===============================

const addRules = {
  name: [
    {
      required: true,
      message: '请输入商品名称',
      trigger: 'blur'
    }
  ],

  price: [
    {
      required: true,
      message: '请输入商品价格',
      trigger: 'blur'
    }
  ],

  number: [
    {
      required: true,
      message: '请输入商品数量',
      trigger: 'blur'
    }
  ],

  weight: [
    {
      required: true,
      message: '请输入商品权重',
      trigger: 'blur'
    }
  ]
}

// ===============================
// 分类
// ===============================

const cateIdList = ref([])

const selectKeys = ref([])

// ===============================
// 商品属性
// ===============================

const attrStatic = ref([])

const attrDynamic = ref([])

// ===============================
// 图片预览
// ===============================

const previewVisible = ref(false)

const previewPath = ref('')

// ===============================
// 初始化
// ===============================

onMounted(() => {
  getCateIDList()
})

// ===============================
// 获取商品分类
// ===============================

async function getCateIDList () {
  try {
    const { data: resp } =
      await getCategoryListApi()

    if (resp.status !== 200) {
      ElMessage.error(resp.msg)
      return
    }

    cateIdList.value =
      resp.data.data
  } catch (error) {
    console.error(
      '获取商品分类失败：',
      error
    )

    ElMessage.error(
      '获取商品分类失败'
    )
  }
}

// ===============================
// 分类选择
// ===============================

function changeSelector () {
  if (selectKeys.value.length < 3) {
    return
  }

  addForm.cid_one =
    selectKeys.value[0]

  addForm.cid_two =
    selectKeys.value[1]

  addForm.cid_three =
    selectKeys.value[2]

  console.log(
    '商品分类：',
    selectKeys.value
  )
}

// ===============================
// Tabs切换
// ===============================

function handleTabChange (activeName) {
  console.log('当前 Tab：', activeName)
  console.log('当前分类：', selectKeys.value)

  // 非基本信息 Tab 必须选择三级分类
  if (
    activeName !== '0' &&
    selectKeys.value.length < 3
  ) {
    ElMessage.error('请选择完整的商品分类！！')

    active.value = '0'

    return
  }

  // 静态参数
  if (activeName === '1') {
    getAttribute('static')
  }

  // 动态参数
  if (activeName === '2') {
    getAttribute('dynamic')
  }
}

// ===============================
// 获取商品属性
// ===============================

async function getAttribute (type) {
  try {
    console.log('获取属性类型：', type)
    console.log('三级分类ID：', selectKeys.value[2])

    const { data: resp } =
      await getAttributeListApi({
        cid: selectKeys.value[2],
        _type: type
      })

    console.log('属性接口返回：', resp)

    if (resp.status !== 200) {
      ElMessage.error(resp.msg)
      return
    }

    // 静态属性
    if (type === 'static') {
      console.log('静态属性原始数据：', resp.data)

      attrStatic.value = resp.data.map(item => ({
        ...item,
        val: item.val || ''
      }))

      console.log('attrStatic：', attrStatic.value)

      return
    }

    // 动态属性
    attrDynamic.value = resp.data.map(item => ({
      ...item,
      options: item.val
        ? item.val.split(',').filter(Boolean)
        : [],
      selected: []
    }))
  } catch (error) {
    console.error('获取商品属性失败：', error)
    ElMessage.error('获取商品属性失败')
  }
}

// ===============================
// 图片上传成功
// ===============================

function handleSuccess (resp) {
  if (
    resp.status &&
    resp.status !== 200
  ) {
    ElMessage.error(
      resp.msg || '图片上传失败'
    )

    return
  }

  if (
    resp.data &&
    resp.data.path
  ) {
    addForm.pics.push(
      resp.data.path
    )
  }
}

// ===============================
// 删除图片
// ===============================

function handleRemove (file) {
  const path =
    file?.response?.data?.path

  if (!path) {
    return
  }

  const index =
    addForm.pics.findIndex(
      item => item === path
    )

  if (index !== -1) {
    addForm.pics.splice(
      index,
      1
    )
  }
  console.log(file)
}

// ===============================
// 图片预览
// ===============================

function handlePreview (file) {
  const url =
    file?.response?.data?.url

  if (!url) {
    return
  }

  previewPath.value = url

  previewVisible.value = true
}

// ===============================
// 添加商品
// ===============================

async function goodsAdd () {
  // 表单验证
  const valid =
    await addRef.value.validate()

  if (!valid) {
    ElMessage.error(
      '请填写必要的参数！！'
    )

    return
  }

  // 检查商品分类
  if (
    selectKeys.value.length < 3
  ) {
    ElMessage.error(
      '请选择完整的商品分类！！'
    )

    active.value = '0'

    return
  }

  // ==========================
  // 静态参数
  // ==========================

  const staticList =
    attrStatic.value.map(item => ({
      id: item.id,
      val: item.val
    }))

  addForm.attr_static =
    JSON.stringify(
      staticList
    )

  // ==========================
  // 动态参数
  // ==========================

  const dynamicList =
    attrDynamic.value.map(item => ({
      id: item.id,

      val: item.selected.join(',')
    }))

  addForm.attr_dynamic =
    JSON.stringify(
      dynamicList
    )

  // ==========================
  // 商品图片
  // ==========================

  addForm.pics =
    JSON.stringify(
      addForm.pics
    )

  console.log(
    '提交商品：',
    addForm
  )

  await saveGoods()
}

// ===============================
// 保存商品
// ===============================

async function saveGoods () {
  try {
    const { data: resp } =
      await axios.post(
        '/goods',
        new URLSearchParams(
          addForm
        )
      )

    if (resp.status !== 200) {
      ElMessage.error(
        resp.msg
      )

      return
    }

    ElMessage.success(
      resp.msg
    )
  } catch (error) {
    console.error(error)

    ElMessage.error(
      '商品添加失败'
    )
  }
}
</script>

<style scoped>
.el-tabs {
  margin-top: 10px;
}

.el-alert {
  margin-bottom: 10px;
}

.el-cascader {
  width: 500px;
}

.el-checkbox {
  margin: 0 10px 0 0 !important;
}

.pre-img {
  width: 100%;
}

.btn-add {
  margin-top: 10px;
}

.editor-wrapper {
  width: 100%;
  margin-bottom: 60px;
}

.editor-wrapper :deep(.ql-container) {
  min-height: 300px;
}

.editor-wrapper :deep(.ql-editor) {
  min-height: 300px;
}
</style>
