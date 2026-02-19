import pytest
from ..models import Role, UserRole, BusinessObject, AccessRoleRule


@pytest.mark.django_db
class TestAccessRules:
    
    @pytest.fixture
    def setup_roles(self):
        admin_role = Role.objects.create(name="admin", description="Administrator")
        user_role = Role.objects.create(name="user", description="Regular User")
        return admin_role, user_role

    @pytest.fixture
    def setup_business_objects(self):
        users_obj = BusinessObject.objects.create(
            name="Пользователи",
            code="users",
            description="Управление пользователями"
        )
        orders_obj = BusinessObject.objects.create(
            name="Заказы",
            code="orders",
            description="Управление заказами"
        )
        return users_obj, orders_obj

    def test_admin_has_all_permissions(self, auth_client, admin_user, setup_roles, setup_business_objects):
        admin_role, _ = setup_roles
        users_obj, _ = setup_business_objects
        
        UserRole.objects.create(user=admin_user, role=admin_role)
        
        AccessRoleRule.objects.create(
            role=admin_role,
            business_object=users_obj,
            read_permission=True,
            read_all_permission=True,
            create_permission=True,
            update_permission=True,
            update_all_permission=True,
            delete_permission=True,
            delete_all_permission=True
        )
        
        rule = AccessRoleRule.objects.get(role=admin_role, business_object=users_obj)
        assert rule.read_permission is True
        assert rule.delete_permission is True

    def test_user_limited_permissions(self, auth_client, user, setup_roles, setup_business_objects):
        _, user_role = setup_roles
        _, orders_obj = setup_business_objects
        
        UserRole.objects.create(user=user, role=user_role)
        
        AccessRoleRule.objects.create(
            role=user_role,
            business_object=orders_obj,
            read_permission=True,
            read_all_permission=False,
            create_permission=True,
            update_permission=True,
            update_all_permission=False,
            delete_permission=False,
            delete_all_permission=False
        )
        
        rule = AccessRoleRule.objects.get(role=user_role, business_object=orders_obj)
        assert rule.read_permission is True
        assert rule.delete_permission is False
