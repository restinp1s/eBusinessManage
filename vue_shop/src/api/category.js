import request from '@/utils/request'
import qs from 'qs'

// 获取商品分类列表
export function getCategoryListApi (params) {
  return request.get('/category_list', {
    params
  })
}

// 新增商品分类
export function addCategoryApi (data) {
  return request.post('/category', qs.stringify(data), {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
}

// 删除商品分类
export function deleteCategoryApi (id) {
  return request.delete(`/category/${id}`)
}

// 获取分类属性
export function getAttributeListApi (params) {
  return request.get('/category/attr_list', {
    params
  })
}
