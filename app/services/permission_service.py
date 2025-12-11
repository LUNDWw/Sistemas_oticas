"""
Permission Management Service
Handles roles and permissions
"""
from app.models import get_db


def get_all_roles():
    """Get all roles"""
    db = get_db()
    roles = db.execute('SELECT * FROM roles ORDER BY name').fetchall()
    return [dict(r) for r in roles]


def get_all_permissions():
    """Get all permissions"""
    db = get_db()
    permissions = db.execute('SELECT * FROM permissions ORDER BY resource, action').fetchall()
    return [dict(p) for p in permissions]


def get_role_permissions(role_id):
    """Get all permissions for a role"""
    db = get_db()
    
    permissions = db.execute('''
        SELECT p.*
        FROM permissions p
        JOIN role_permissions rp ON p.id = rp.permission_id
        WHERE rp.role_id = ?
    ''', (role_id,)).fetchall()
    
    return [dict(p) for p in permissions]


def update_role_permissions(role_id, permission_ids):
    """Update permissions for a role"""
    db = get_db()
    
    # Check if role is system role
    role = db.execute('SELECT is_system FROM roles WHERE id = ?', (role_id,)).fetchone()
    if role and role['is_system']:
        raise ValueError("Não é possível modificar permissões de roles do sistema")
    
    # Remove existing permissions
    db.execute('DELETE FROM role_permissions WHERE role_id = ?', (role_id,))
    
    # Add new permissions
    for perm_id in permission_ids:
        db.execute('''
            INSERT INTO role_permissions (role_id, permission_id)
            VALUES (?, ?)
        ''', (role_id, perm_id))
    
    db.commit()


def get_permissions_by_resource():
    """Get permissions grouped by resource"""
    db = get_db()
    permissions = db.execute('''
        SELECT * FROM permissions 
        ORDER BY resource, action
    ''').fetchall()
    
    # Group by resource
    grouped = {}
    for perm in permissions:
        resource = perm['resource']
        if resource not in grouped:
            grouped[resource] = []
        grouped[resource].append(dict(perm))
    
    return grouped
