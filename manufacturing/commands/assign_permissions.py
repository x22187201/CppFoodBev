from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from manufacturing.models import CustomAdmin  # Replace 'your_app' with the actual name of your app

class Command(BaseCommand):
    help = 'Assign permissions to a CustomAdmin user'

    def handle(self, *args, **options):
        # Replace 'desired_permission_codename' with the actual codename of the permission
        desired_permission_codename = 'add_product'

        # Check if the permission exists
        try:
            permission = Permission.objects.get(codename=desired_permission_codename)
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Permission with codename '{desired_permission_codename}' does not exist."))
            return

        # Replace 'admin_username' with the username of the CustomAdmin instance
        admin_username = 'admin_username'

        # Check if the admin user exists
        try:
            admin_user = CustomAdmin.objects.get(username=admin_username)
        except CustomAdmin.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Admin user with username '{admin_username}' does not exist."))
            return

        # Assign the permission to the admin user
        admin_user.user_permissions.add(permission)

        self.stdout.write(self.style.SUCCESS(
            f"Permission '{desired_permission_codename}' assigned to admin user '{admin_username}'."
        ))
