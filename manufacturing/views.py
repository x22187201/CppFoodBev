# Import necessary modules and serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Ingredient, Cart, Order
from django.contrib.auth.models import Group
from .serializers import ProductSerializer, IngredientSerializer
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404
from .map_api import MapAPI
from .models import Order  # Import your Order model
import boto3
from django.conf import settings
from django.http import HttpResponse



sns = boto3.client(
    "sns",
    region_name="eu-west-1",  # Replace 'your_region' with your AWS region
    aws_access_key_id="ASIATUYJP7SUJH7SMVEZ",  # Replace 'your_access_key' with your AWS access key
    aws_secret_access_key="MdegO25fZLQNHo1TroBRxgR7wJY9qbfZDAyAPM64",  # Replace 'your_secret_key' with your AWS secret key
    aws_session_token = "IQoJb3JpZ2luX2VjEIL//////////wEaCXVzLWVhc3QtMSJHMEUCICYCnupmdgrC9Sdpcx8K6MBaBB+2J3Ac6oOFqDoSOQaWAiEAqpcLZCOiFB2eehP4bJwl+ZBIGYy+JYdN5R9IiGFrpPIqhAQI2v//////////ARADGgwyNTA3Mzg2Mzc5OTIiDPAGd6dFoWrnPpJLmyrYA/Z/3YFhI//mjx3HudFLqksK/fAE6751OBXIC9FMSba75l/eCoYA+Nfvhsr9YcvZMRi/o9WqWLLIsmtmvoZPDaRytTllF4ka118OuYKtwTmaHp5xjqfeOmXkaW6mDrhj0TrCvJ7D95X553CkFJA/yLX/dg0ivI2a+VFrGMNi/yg/ZzAJSU7YAp8O44e55BnEbro70e06kF7neyltATEdS6iKj2ZvlPr3/XWa/41mjLAkBpyb3rIe589CAoItC71gK9eT5WjYbP3Hdms4MNupTON7M8GGn8Jkpkl8hW0m0Ppg1QtULAYV4gsusGAHpTzngBkAr8FJPpfXCIx7xnabCuW73yQJeKoG6zn5IvBonqexVrTqH5XOrphUaJnSgTF44cJTTeHGTOKYwBwAkgzVRYz4CNSC9sp8432ej/wsf+0HAzxszBxUGVXY0iPqvnaZ4ooTBP3jcgopm5d2P4ENjLFC/zaHaSgRapSuvSfiQq2yVuL74AJXk6IVhi2ZEV+oK2w2S7NYUVHQ4KM63ejHvVIhSZczaycfWPBCdJr+Boq04Qr+4rczVIz6BtK9Mus3dY1Q6uO/tv9WnR+5HZEBeOAK+5TQZFi48NuVrD+h1tUxA6fTvGkSsUcwiOKdqwY6pgHwsC+89KY9iiC7G4eeOu7tDrxeunva6YjSxxgLWLZrTG4noOMbxKh7X9pKZUdd8mxY5GjrwQOaoIZxrFBK+TSqYbJomNM3Peued4+/mIkblBIyE8CoygkJaHLMAKI14QAdxxL60zfEG/mfeUHWmoVdFn0vjcEJgIK2DG3iguUi6OuSUhd/ESOXw51Wv2TFENnQGbOtmdzuMDDfdyT+A+mDgPRbHGe8"
    )
    
SNS_TOPIC_ARN = "arn:aws:sns:eu-west-1:250738637992:x22187201Register"

# Product Views
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Ingredient Views
@api_view(['GET', 'POST'])
def ingredient_list(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def ingredient_detail(request, pk):
    try:
        ingredient = Ingredient.objects.get(pk=pk)
    except Ingredient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@login_required
def list_all_products(request):
    products = Product.objects.all()  # Retrieve all products
    serializer = ProductSerializer(products, many=True)
    print(products)
    for product in serializer.data:
        print(f"Product Name: {product['name']}, Image URL: {product['product_image']}")
        # print(product['name'])

    return render(request, 'product_list.html', {'products': serializer.data})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Cart

@login_required
def view_cart(request):
    try:
        user_cart = Cart.objects.get(user=request.user)
        cart_items = user_cart.products.all()  # Retrieve products associated with the user's cart
        print('keshav')
        print(cart_items)
        for i in cart_items:
            print(i.unit_price)
        return render(request, 'cart.html', {'cart_items': cart_items})
    except Cart.DoesNotExist:
        return render(request, 'cart.html', {'error_message': 'Cart not found'})


@login_required
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        user_cart.products.add(product)
        return JsonResponse({'message': 'Product added to the cart'}, status=200)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
@login_required
def remove_from_cart(request, product_id):
    print("Helllo remove_from_cart called")
    product = Product.objects.get(pk=product_id)
    user_cart = Cart.objects.get(user=request.user)
    user_cart.products.remove(product)
    return redirect('view_cart')

# @login_required
def get_cart_items(request):
    user = request.user

    # Retrieve the user's cart
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return JsonResponse({'message': 'Cart not found'}, status=404)

    # Get the products in the user's cart
    cart_items = cart.products.all()

    # Serialize the cart items to a list of dictionaries
    cart_item_list = [
        {
            'id': item.id,
            'name': item.name,
            'unit_price': item.unit_price,
        }
        for item in cart_items
    ]
    print(cart_item_list)
    return JsonResponse({'cart_items': cart_item_list})

from .forms import OrderForm  # Import the OrderForm from the previous step

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Cart, Order, Product
import json

@require_POST
@ensure_csrf_cookie
def place_order(request):
    user = request.user
    print(user)
    if not user.is_authenticated:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)

    data = json.loads(request.body)
    delivery_address = data.get('delivery_address')
    pincode = data.get('pincode')
    country = data.get('country')
    # Create an Order instance but don't save it yet
    order = Order(user=user, delivery_address=delivery_address, pincode=pincode, country=country)
    print(order)
    # Retrieve products from the user's cart
    cart = Cart.objects.get(user=user)
    products = cart.products.all()

    # Calculate the total price based on associated products
    total_price = sum(product.unit_price for product in products)
    print(total_price)

    # Set the calculated total price
    order.total_price = total_price

    # Save the order to the database
    order.save()

    # Now that the order is saved, you can associate the products with it
    order.products.set(products)

    # Clear the user's cart by removing all products
    cart.products.clear()
    print('DONE')
    return JsonResponse({'message': 'Order placed successfully'})

def home(request):
    return render(request, 'home.html')
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

from .models import Product
from .forms import ProductForm  # Import the form you'll create

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        print('In add_Product')
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to the admin dashboard after successful product addition
        else:
            print(form.errors)
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

from .forms import IngredientForm

@login_required
def add_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Adjust the URL name as needed
    else:
        form = IngredientForm()
    
    return render(request, 'add_ingredient.html', {'form': form})

# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order

# views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order, CustomUser

@login_required
# @user_passes_test(lambda u: u.is_staff, login_url='admin_dashboard')  # Ensure user is staff (CustomAdmin)
def view_orders(request, user_id=None):
    # print(user)
    if user_id is not None:
        user = get_object_or_404(CustomUser, id=user_id)
        orders = Order.objects.filter(user=user)
    else:
        # If user_id is not provided, show all orders
        print('all orders')
        orders = Order.objects.all()
        print(orders)

    return render(request, 'view_orders.html', {'orders': orders})

@login_required

def view_products(request):
    products = Product.objects.all()
    return render(request, 'view_products.html', {'products': products})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    print('In delete')
    print(request.method)
    if request.method == 'POST':
        product.delete()
        print('YEss')
        return redirect('view_products')

    return render(request, 'admin_dashboard.html', {'product': product})
# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, AdminRegistrationForm, UserLoginForm, AdminLoginForm
from .models import CustomUser, CustomAdmin

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f"New User added",)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_login')  # Redirect to the home page after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'user_register.html', {'form': form})

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            admin = authenticate(username=username, password=raw_password)
            login(request, admin)
            return redirect('admin_login')  # Redirect to the admin home page after successful registration
    else:
        form = AdminRegistrationForm()
    return render(request, 'admin_register.html', {'admin_form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None and not user.is_admin:
                login(request, user)
                return redirect('list_all_products')  # Redirect to the home page after successful login
    else:
        form = UserLoginForm()
    return render(request, 'user_login.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            admin = authenticate(request, username=username, password=password)
            print(admin.__class__.__mro__[0].__name__)
            print(admin)
            print(isinstance(admin, CustomAdmin))
            print(form.Meta.model.__name__)
            
            if admin is not None and admin.is_admin:
                login(request, admin)
                return redirect('admin_dashboard')  # Redirect to the admin home page after successful login

    else:
        form = AdminLoginForm()
    return render(request, 'admin_login.html', {'admin_form': form})




def optimized_route_view(request, user_id=None):
    if user_id is not None:
        user = get_object_or_404(CustomUser, id=user_id)
        orders = Order.objects.filter(user=user)
    else:
        orders = Order.objects.all()

    waypoints = [order.delivery_address for order in orders]
    print("printing waypoints")
    print(waypoints)
    api_key = "AIzaSyDJEGAeKc_U4sgA0K3a86brTATczFx_rpQ"
    map_api = MapAPI(api_key)
    optimized_route = map_api.get_optimized_route(waypoints)
    print('keshav')
    print(optimized_route)

    origin = waypoints[0]
    destination = waypoints[-1]
    distance, duration = map_api.get_route_distance_duration(origin, destination)
    print('singh')
    print(distance, duration)
    
    # Example geocoding
    geocoded_coordinates = {}
    for waypoint in waypoints:
        latitude, longitude = map_api.geocode_address(waypoint)
        geocoded_coordinates[waypoint] = {"latitude": latitude, "longitude": longitude}
    print(geocoded_coordinates)
    
    context = {
        'optimized_route': optimized_route,
        'distance': distance,
        'duration': duration,
        'geocoded_coordinates': geocoded_coordinates,
    }

    print(context)
    return render(request, 'optimized_route.html', {'optimized_route': context})
