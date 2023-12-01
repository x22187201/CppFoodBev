from django.urls import path
from . import views
from .views import optimized_route_view

urlpatterns = [

    path('', views.home, name='home'),  # Home page

    # URLs for the Product model
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),

    # URLs for the Ingredient model
    path('ingredients/', views.ingredient_list, name='ingredient-list'),
    path('ingredients/<int:pk>/', views.ingredient_detail, name='ingredient-detail'),

    # Cart Views
    path('view_cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('list_all_products/', views.list_all_products, name='list_all_products'),
    path('get_cart_items/', views.get_cart_items, name='get_cart_items'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_ingredient/', views.add_ingredient, name='add_ingredient'),
    path('view_products/', views.view_products, name='view_products'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('user_register/', views.user_register, name='user_register'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('user/login/', views.user_login, name='user_login'),
    path('admin_login/', views.admin_login, name='admin_login'),
        path('logout/', views.user_logout, name='logout'),


    path('optimized-route/', views.optimized_route_view, name='optimized_route'),


]
