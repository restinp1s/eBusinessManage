import request from '@/utils/request'

// 获取订单列表
export function getOrderListApi (params) {
  return request.get('/order_list', {
    params
  })
}

// 获取订单物流信息
export function getExpressListApi (params) {
  return request.get('/express', {
    params
  })
}
