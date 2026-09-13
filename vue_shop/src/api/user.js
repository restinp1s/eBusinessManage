import request from '@/utils/request'

// 获取用户列表

// 新增用户

export function addUserApi (data) {
  return request.post(
    '/user/user',
    data,
    {
      headers: {
        'Content-Type': 'application/json'
      }
    }
  )
}

export function getUserListApi (params) {
  return request.get(
    '/user/user_list',
    {
      params
    }
  )
}

export function updateUserApi (data) {
  return request.put(

    '/user/user',

    data

  )
}

// 删除用户
export function deleteUserApi (data) {
  return request.delete(
    '/user/user',
    {
      data
    }
  )
}
