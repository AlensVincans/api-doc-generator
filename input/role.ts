import { Router } from 'express'
import { RoleController } from '../controllers/role.controller'
import { RoleService } from '../services/role.service'
import { RoleRepository } from '../repositories/role.repository'
import {
  isAuthenticated,
  requirePermission,
  requireRole,
  requireAnyRole,
} from '../middlewares/auth.middleware'
import { Permission, Role } from '../types/rbac.types'

export default (router: Router) => {
  // Initialize Dependency Injection
  const roleRepository = new RoleRepository()
  const roleService = new RoleService(roleRepository)
  const roleController = new RoleController(roleService)

  

  
  router.get(
    '/roles',
    isAuthenticated,
    requirePermission(Permission.ROLE_LIST),
    roleController.getAllRoles,
  )

  
  router.get(
    '/roles/:name',
    isAuthenticated,
    requirePermission(Permission.ROLE_READ),
    roleController.getRoleByName,
  )

  
  router.post(
    '/roles',
    isAuthenticated,
    requireAnyRole([Role.SUPER_ADMIN]),
    requirePermission(Permission.ROLE_CREATE),
    roleController.createRole,
  )

  
  router.put(
    '/roles/:name/permissions',
    isAuthenticated,
    requireAnyRole([Role.SUPER_ADMIN]),
    requirePermission(Permission.PERMISSION_ASSIGN),
    roleController.updateRolePermissions,
  )

  
  router.post(
    '/roles/:name/permissions/add',
    isAuthenticated,
    requireAnyRole([Role.SUPER_ADMIN]),
    requirePermission(Permission.PERMISSION_ASSIGN),
    roleController.addPermissions,
  )

  
  router.post(
    '/roles/:name/permissions/remove',
    isAuthenticated,
    requireAnyRole([Role.SUPER_ADMIN]),
    requirePermission(Permission.PERMISSION_ASSIGN),
    roleController.removePermissions,
  )

  
  router.delete(
    '/roles/:name',
    isAuthenticated,
    requireAnyRole([Role.SUPER_ADMIN]),
    requirePermission(Permission.ROLE_DELETE),
    roleController.deleteRole,
  )

  
}
