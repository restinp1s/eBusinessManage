<template>
    <div>
      <!-- 面包屑 -->
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/home' }">
          首页
        </el-breadcrumb-item>

        <el-breadcrumb-item>
          订单管理
        </el-breadcrumb-item>

        <el-breadcrumb-item>
          订单列表
        </el-breadcrumb-item>
      </el-breadcrumb>

      <el-card>
        <!-- 搜索区域 -->
        <el-row>
          <el-col :span="8">
            <el-input
              v-model="qid"
              placeholder="请输入订单ID"
              clearable
              @clear="getOrderList"
            >
              <template #append>
                <el-button @click="getOrderList">
                  <el-icon>
                    <Search />
                  </el-icon>
                </el-button>
              </template>
            </el-input>
          </el-col>
        </el-row>

        <!-- 订单表格 -->
        <el-row>
          <el-table
            :data="orderList"
            border
            style="width: 100%"
          >
            <!-- 序号 -->
            <el-table-column
              type="index"
              label="#"
              width="60"
              align="center"
            />

            <!-- 订单ID -->
            <el-table-column
              prop="id"
              label="ID"
              width="80"
              align="center"
            />

            <!-- 订单用户 -->
            <el-table-column
              prop="uname"
              label="订单用户"
              min-width="120"
            />

            <!-- 金额 -->
            <el-table-column
              prop="price"
              label="金额"
              width="120"
            />

            <!-- 支付状态 -->
            <el-table-column
              label="是否支付"
              width="120"
              align="center"
            >
              <template #default="{ row }">
                <el-tag
                  v-if="row.pay_status === 0"
                  type="danger"
                >
                  未支付
                </el-tag>

                <el-tag
                  v-else
                  type="success"
                >
                  已支付
                </el-tag>
              </template>
            </el-table-column>

            <!-- 发货状态 -->
            <el-table-column
              label="是否发件"
              width="120"
              align="center"
            >
              <template #default="{ row }">
                <el-tag
                  v-if="row.is_send === 0"
                  type="danger"
                >
                  未发件
                </el-tag>

                <el-tag
                  v-else
                  type="success"
                >
                  已发件
                </el-tag>
              </template>
            </el-table-column>

            <!-- 操作 -->
            <el-table-column
              label="操作"
              width="200"
              align="center"
            >
              <template #default="{ row }">
                <!-- 地址 -->
                <el-button
                  size="small"
                  type="primary"
                  @click="showAddress(row)"
                >
                  <el-icon>
                    <Location />
                  </el-icon>
                  地址
                </el-button>

                <!-- 物流 -->
                <el-button
                  size="small"
                  type="success"
                  @click="showExpress(row.id)"
                >
                  <el-icon>
                    <Van />
                  </el-icon>
                  物流
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-row>
      </el-card>

      <!-- 物流弹窗 -->
      <el-dialog
        v-model="expressVisible"
        title="物流信息"
        width="600px"
      >
        <!-- 有物流信息 -->
        <el-timeline
          v-if="expressList.length > 0"
          :reverse="reverse"
        >
          <el-timeline-item
            v-for="(activity, index) in expressList"
            :key="index"
            :timestamp="activity.update_time"
          >
            {{ activity.content }}
          </el-timeline-item>
        </el-timeline>

        <!-- 没有物流信息 -->
        <el-empty
          v-else
          description="暂无物流信息"
        />
      </el-dialog>
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
  Search,
  Location,
  Van
} from '@element-plus/icons-vue'

import {
  getOrderListApi,
  getExpressListApi
} from '@/api/order'

// 搜索订单ID
const qid = ref('')

// 订单列表
const orderList = ref([])

// 物流弹窗显示状态
const expressVisible = ref(false)

// 物流列表
const expressList = ref([])

// 时间线是否反向
const reverse = ref(false)

// 获取订单列表
const getOrderList = async () => {
  try {
    const { data: resp } = await getOrderListApi({
      id: qid.value
    })

    console.log('订单接口返回：', resp)

    if (resp.status !== 200) {
      ElMessage.error(resp.msg || '获取订单列表失败')
      return
    }

    orderList.value = resp.data || []

    console.log('订单列表：', orderList.value)
  } catch (error) {
    console.error('获取订单列表失败：', error)
    ElMessage.error('获取订单列表失败')
  }
}

// 显示收货地址
const showAddress = (row) => {
  if (!row.addrs) {
    ElMessage.info('暂无收货地址')
    return
  }

  ElMessage.info(`收货地址：${row.addrs}`)
}

// 显示物流
const showExpress = async (oid) => {
  // 打开弹窗
  expressVisible.value = true

  // 清空上一次物流数据
  expressList.value = []

  // 获取物流
  await getExpressList(oid)
}

// 获取物流列表
const getExpressList = async (oid) => {
  try {
    const { data: resp } = await getExpressListApi({
      oid: oid
    })

    console.log('物流接口返回：', resp)

    if (resp.status !== 200) {
      ElMessage.error(resp.msg || '获取物流信息失败')
      return
    }

    expressList.value = resp.data || []

    console.log('物流列表：', expressList.value)
  } catch (error) {
    console.error('获取物流信息失败：', error)
    ElMessage.error('获取物流信息失败')
  }
}

// 页面加载时获取订单列表
onMounted(() => {
  getOrderList()
})
</script>

  <style scoped>
  .el-table {
    margin-top: 10px;
  }
  </style>
