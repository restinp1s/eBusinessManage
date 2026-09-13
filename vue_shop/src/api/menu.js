import request from '../utils/request'
// 删除角色权限

export function deleteMenuApi (data) {
  return request.delete(

    '/role/menu',

    {
      params: data
    }

  )
}

// 获取菜单

export function getMenuApi (params) {
  return request.get(

    '/menu',

    {
      params
    }

  )
}

// 分配权限

export function setRoleMenuApi (data) {
  return request.post(

        `/role/set_menu/${data.rid}`,

        `mids=${data.mids}`,

        {
          headers: {
            'Content-Type':
                'application/x-www-form-urlencoded'
          }
        }

  )
}
