from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput
from .models import CustomUser, CustomAdmin
from .models import Order
from .models import Product

# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, CustomAdmin

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    u_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'u_name', 'phone_number', 'password1', 'password2']

class AdminRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    u_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = CustomAdmin
        fields = ['username', 'email', 'u_name', 'phone_number', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class AdminLoginForm(AuthenticationForm):
    class Meta:
        model = CustomAdmin
        fields = ['username', 'password']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'pincode', 'country']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'manufacturing_date': DateInput(attrs={'type': 'date'}),
            'expiration_date': DateInput(attrs={'type': 'date'}),
        }
    product_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Product Image')


from .models import Ingredient

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'description', 'supplier', 'lot_number', 'quantity', 'unit_price', 'product']
        
        # You can customize widgets or add validation if needed
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'product': forms.Select(attrs={'class': 'browser-default'}), 
              # Using 'browser-default' class for Materialize dropdown
        }

    def __init__(self, *args, **kwargs):
        super(IngredientForm, self).__init__(*args, **kwargs)
        # Populate the product dropdown with choices from the Product model
        self.fields['product'].queryset = Product.objects.all()