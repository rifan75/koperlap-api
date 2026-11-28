from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rbac.models.role import Role
from app.core.rbac.models.permission import Permission

from app.core.rbac.models.principal_role import MemberRole
from app.core.rbac.models.principal_role import ClientRole
from app.core.rbac.models.principal_role import AdminRole
from app.core.rbac.models.role_permission import RolePermission 

from app.core.principal import Principal

# This produces:
# {
#   "roles": ["admin", "manager"],
#   "permissions": [
#     "reports.read",
#     "users.read",
#     "users.write"
#   ]
# }


ROLE_MODELS = {
    "member": (MemberRole, "member_id"),
    "client": (ClientRole, "client_id"),
    "admin": (AdminRole, "admin_id"),
}


async def get_user_authorities(
    db: AsyncSession,
    principal: Principal,
):
    config = ROLE_MODELS.get(principal.type)

    if config is None:
        raise ValueError("Unsupported principal type")

    role_model, principal_field = config

    principal_column = getattr(
        role_model,
        principal_field,
    )

    stmt = (
        select(
            Role.name,
            Permission.code,
        )
        .select_from(role_model)
        .join(
            Role,
            Role.id == role_model.role_id,
        )
        .outerjoin(
            RolePermission,
            RolePermission.role_id == Role.id,
        )
        .outerjoin(
            Permission,
            Permission.id == RolePermission.permission_id,
        )
        .where(
            principal_column == principal.id,
        )
    )

    result = await db.execute(stmt)

    rows = result.all()

    roles = sorted({
        row.name for row in rows
    })

    permissions = sorted({
        row.code
        for row in rows
        if row.code is not None
    })

    return roles, permissions