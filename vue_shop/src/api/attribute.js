import request from '@/utils/request'
import qs from 'qs'

export function addAttributeApi (data) {
  return request.post(
    '/category/attribute',
    qs.stringify(data)
  )
}

// 获取分类
export function getCategoryListApi () {
  return request.get('/category_list')
}

// 获取分类参数
export function getAttributeListApi (params) {
  return request.get(
    '/category/attr_list',
    {
      params
    }
  )
}

// 新增属性

// 修改属性
export function updateAttributeApi (data) {
  return request.put(
    '/category/attribute',
    qs.stringify(data)
  )
}

export function deleteAttributeApi (id) {
  return request.delete(
    '/category/attribute',
    {
      headers: {
        'Content-Type':
          'application/x-www-form-urlencoded'
      },

      data: qs.stringify({
        id: id
      })

    }
  )
}

export function getAttributeDetailApi (id) {
  return request.get(
    '/category/attribute',
    {
      params: {
        id
      }
    }
  )
}
