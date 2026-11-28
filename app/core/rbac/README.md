#Assign a role to a member: 
<pre>
member.roles.append(
       MemberRole(role_id=1)
)
await db.commit()
</pre>

#Assign a role to a admin: 
<pre>
admin.roles.append(
       AdminRole(role_id=1)
)
await db.commit()
</pre>

#Assign a role to a client:
<pre>
client.roles.append(
    ClientRole(role_id=2)
)
await db.commit()
</pre>

#Example retrieve roles for principal
<pre>
member = await db.get(Member, member_id)

for assignment in member.roles:
       print(assignment.role.name)
</pre>
  
                  ┌──────────────┐
                  │    Role      │
                  ├──────────────┤
                  │ id           │
                  │ name         │
                  │ description  │
                  └──────┬───────┘
                         │
              ┌──────────┴──────────┐
              │                     │
       RolePermission          MemberRole
              │                     │
              ▼                     ▼
         Permission              Member
              ▲
              │
       RolePermission
              │
              └── ClientRole
              └── AdminRole