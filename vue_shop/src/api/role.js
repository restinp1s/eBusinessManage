import request from '../utils/request'

// 角色列表

export function getRoleListApi () {
  return request.get(
    '/role/role_list'
  )
}

// 新增角色

export function addRoleApi (data) {
  return request.post(
    '/role/role',
    data
  )
}

// 修改角色

export function updateRoleApi (data) {
  return request.put(
    '/role/role',
    data
  )
}

// 删除角色

export function deleteRoleApi (data) {
  return request.delete(
    '/role/role',
    {
      data
    }
  )
}
