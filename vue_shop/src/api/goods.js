import request from '@/utils/request'

// 获取商品列表
export function getGoodsListApi (params) {
  return request({
    url: '/goods_list',
    method: 'get',
    params
  })
}

// 删除商品
export function deleteGoodsApi (data) {
  return request({
    url: '/goods',
    method: 'delete',
    data
  })
}

// 获取商品详情
export function getGoodsApi (params) {
  return request({
    url: '/goods',
    method: 'get',
    params
  })
}

// 新增商品
export function addGoodsApi (data) {
  return request({
    url: '/goods',
    method: 'post',
    data
  })
}

// 修改商品
export function updateGoodsApi (data) {
  return request({
    url: '/goods',
    method: 'put',
    data
  })
}
