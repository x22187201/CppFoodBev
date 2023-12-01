from django.contrib.auth.models import AbstractUser,Permission
from django.contrib.auth.models import Group  # Import the Group model

from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # User's email address
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # User's phone number
    cart = models.OneToOneField('Cart', on_delete=models.SET_NULL, null=True, blank=True)  # User's cart

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        related_query_name='customuser',
    )

    # Add a related_name for the groups field
    groups = models.ManyToManyField(Group, related_name='customuser_set', related_query_name='customuser',  blank=True)
    class Meta:
        permissions = [
            ("view_orders", "Can view orders"),
        ]
    def __str__(self):
        return self.username
    
    is_admin = models.BooleanField(default=False)

class CustomAdmin(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # Set is_admin to True for admin users
        self.is_admin = True
        super().save(*args, **kwargs)
    
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    manufacturing_date = models.DateField()
    expiration_date = models.DateField()
    batch_number = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='product_images/')
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    supplier = models.CharField(max_length=100)
    lot_number = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredients', default=1)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='carts')
    products = models.ManyToManyField(Product)

from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    def calculate_total_price(self):
        return sum(product.unit_price for product in self.products.all())
    
    def save(self, *args, **kwargs):
        if self.total_price is None:
            self.total_price = self.calculate_total_price()
        super(Order, self).save(*args, **kwargs)
    def __str__(self):
        return f'Order by {self.user}'
