from django.contrib import admin
from .models import Product, Ingredient, CustomUser, Cart, Order, CustomAdmin

admin.site.register(Product)
admin.site.register(Ingredient)
admin.site.register(CustomUser)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(CustomAdmin)
