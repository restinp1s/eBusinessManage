
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
        商品列表
      </el-breadcrumb-item>
    </el-breadcrumb>

    <el-card class="goods-card">
      <!-- 搜索和新增 -->
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="qname"
            placeholder="请输入搜索名称"
            clearable
            @clear="getGoodsList"
            @keyup.enter="getGoodsList"
          >
            <template #append>
              <el-button @click="getGoodsList">
                <el-icon>
                  <Search />
                </el-icon>
              </el-button>
            </template>
          </el-input>
        </el-col>

        <el-col :span="4">
          <el-button
            type="primary"
            @click="addGoodsPage"
          >
            <el-icon>
              <Plus />
            </el-icon>
            增加商品
          </el-button>
        </el-col>
      </el-row>

      <!-- 商品表格 -->
      <el-table
        :data="goodsList"
        border
        stripe
        v-loading="loading"
      >
        <!-- 序号 -->
        <el-table-column
          type="index"
          label="#"
          width="60"
        />

        <!-- 商品名称 -->
        <el-table-column
          label="商品名称"
          prop="name"
          min-width="300"
        />

        <!-- 商品价格 -->
        <el-table-column
          label="商品价格(元)"
          prop="price"
          width="120"
        />

        <!-- 商品库存 -->
        <el-table-column
          label="商品库存"
          prop="number"
          width="100"
        />

        <!-- 操作 -->
        <el-table-column
          label="操作"
          width="200"
          fixed="right"
        >
          <template #default="scope">
            <el-button
              size="small"
              type="success"
              @click="editGoods(scope.row.id)"
            >
              <el-icon>
                <Edit />
              </el-icon>
              编辑
            </el-button>

            <el-button
              size="small"
              type="danger"
              @click="removeGoods(scope.row.id)"
            >
              <el-icon>
                <Delete />
              </el-icon>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  ElMessage,
  ElMessageBox
} from 'element-plus'

import {
  getGoodsListApi,
  deleteGoodsApi
} from '@/api/goods'

import {
  Search,
  Plus,
  Edit,
  Delete
} from '@element-plus/icons-vue'

// router
const router = useRouter()

// 商品列表
const goodsList = ref([])

// 搜索商品名称
const qname = ref('')

// 加载状态
const loading = ref(false)

/**
 * 获取商品列表
 */
const getGoodsList = async () => {
  try {
    loading.value = true

    const { data: resp } = await getGoodsListApi({
      name: qname.value
    })

    if (resp.status !== 200) {
      ElMessage.error(resp.msg)
      return
    }

    goodsList.value = resp.data
  } catch (error) {
    console.error('获取商品列表失败:', error)
    ElMessage.error('获取商品列表失败')
  } finally {
    loading.value = false
  }
}

/**
 * 删除商品
 */
const removeGoods = async (gid) => {
  try {
    await ElMessageBox.confirm(
      '此操作将永久删除此商品数据，是否继续？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const { data: resp } = await deleteGoodsApi({
      id: gid
    })

    if (resp.status !== 200) {
      ElMessage.error(resp.msg)
      return
    }

    ElMessage.success(resp.msg)

    // 删除成功后刷新列表
    await getGoodsList()
  } catch (error) {
    // 点击取消
    if (error === 'cancel' || error === 'close') {
      ElMessage.info('已取消删除')
      return
    }

    console.error('删除商品失败:', error)
    ElMessage.error('删除商品失败')
  }
}

/**
 * 新增商品
 */
const addGoodsPage = () => {
  router.push('/add_goods')
}

/**
 * 编辑商品
 */
const editGoods = (gid) => {
  router.push({
    path: '/edit_goods',
    query: {
      id: gid
    }
  })
}

/**
 * 页面加载时获取商品
 */
onMounted(() => {
  getGoodsList()
})

</script>

<style scoped lang="less">
.goods-card {
  margin-top: 15px;
}

.el-table {
  margin-top: 15px;
}
</style>
```
