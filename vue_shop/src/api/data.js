import request from '@/utils/request'

// 获取商品分类统计数据
export function getCateGroupLevelApi () {
  return request.get('/category/cate_group_level')
}
