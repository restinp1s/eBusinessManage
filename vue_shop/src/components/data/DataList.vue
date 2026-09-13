<template>
    <div class="data-page">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/home' }">
          首页
        </el-breadcrumb-item>

        <el-breadcrumb-item>
          数据统计
        </el-breadcrumb-item>

        <el-breadcrumb-item>
          商品统计
        </el-breadcrumb-item>
      </el-breadcrumb>

      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>可视化图表</span>
          </div>
        </template>

        <!-- ECharts 容器 -->
        <div ref="chartRef" class="chart"></div>
      </el-card>
    </div>
  </template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

import { getCateGroupLevelApi } from '@/api/data'

// ECharts DOM
const chartRef = ref(null)

// ECharts 实例
let myChart = null

// 获取统计数据并绘制图表
const getCateGroupLevel = async () => {
  try {
    const { data: resp } = await getCateGroupLevelApi()

    console.log('商品统计接口返回：', resp)

    if (resp.status !== 200) {
      ElMessage.error(resp.msg || '获取商品统计数据失败')
      return
    }

    // 初始化 ECharts
    if (!chartRef.value) {
      return
    }

    myChart = echarts.init(chartRef.value)

    // ECharts 配置
    const option = {
      title: {
        text: '商品分类统计',
        left: 10
      },

      tooltip: {
        trigger: 'axis'
      },

      legend: {
        data: [resp.data.name],
        top: 30
      },

      xAxis: {
        type: 'category',
        data: resp.data.xAxis
      },

      yAxis: {
        type: 'value'
      },

      series: [
        {
          name: resp.data.name,
          type: 'bar',
          data: resp.data.series_data
        }
      ]
    }

    // 设置图表
    myChart.setOption(option)
  } catch (error) {
    console.error('获取商品统计数据失败：', error)
    ElMessage.error('获取商品统计数据失败')
  }
}

// 浏览器窗口变化时重新计算图表大小
const handleResize = () => {
  if (myChart) {
    myChart.resize()
  }
}

// 页面加载
onMounted(() => {
  getCateGroupLevel()

  window.addEventListener('resize', handleResize)
})

// 页面销毁
onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)

  if (myChart) {
    myChart.dispose()
    myChart = null
  }
})
</script>

  <style scoped>
  .data-page {
    width: 100%;
  }

  .chart-card {
    margin-top: 15px;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 25px;
    font-weight: 600;
  }

  .chart {
    width: 100%;
    height: 500px;
  }
  </style>
