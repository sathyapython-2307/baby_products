def pampers_view(request):
    return render(request, 'pampers.html')
# Category pages
def boys_fashion_view(request):
    return render(request, 'boys_fashion.html')

def girls_fashion_view(request):
    return render(request, 'girls_fashion.html')

def soap_view(request):
    return render(request, 'soap.html')

def stroller_view(request):
    return render(request, 'stroller.html')

def bottle_view(request):
    return render(request, 'bottle.html')

def offers_view(request):
    return render(request, 'offers.html')

# About page view
def about_view(request):
    return render(request, 'about.html')

# Contact page view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        # Here you would process the form data, e.g., send email or save to DB
        # For now, just return a success message (AJAX handled in template)
        return JsonResponse({'success': True})
    return render(request, 'contact.html')
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = LoginForm()
    return render(request, 'login_signup.html', {'form': form, 'signup': False})



from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse

# --- CART & CHECKOUT VIEWS ---
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_subtotal = 0
    for pid, item in cart.items():
        subtotal = float(item['price']) * int(item['quantity'])
        cart_items.append({
            'id': pid,
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'image_url': item['image'],
            'subtotal': subtotal,
        })
        cart_subtotal += subtotal
    cart_discount = 250 if cart_items else 0
    cart_total = cart_subtotal - cart_discount
    quantity_range = range(1, 11)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_subtotal': int(cart_subtotal),
        'cart_discount': cart_discount,
        'cart_total': int(cart_total) if cart_total > 0 else 0,
        'quantity_range': quantity_range,
    })

from django.views.decorators.http import require_POST
import uuid

@require_POST
def add_to_cart(request):
    product_name = request.POST.get('product_name')
    product_price = request.POST.get('product_price')
    product_image = request.POST.get('product_image')
    cart = request.session.get('cart', {})
    # Use product_name as the key for simplicity
    if product_name in cart:
        cart[product_name]['quantity'] = int(cart[product_name]['quantity']) + 1
    else:
        cart[product_name] = {
            'name': product_name,
            'price': product_price,
            'quantity': 1,
            'image': product_image,
        }
    request.session['cart'] = cart
    return redirect('cart')

@require_POST
def update_cart(request, item_id):
    from django.http import JsonResponse
    quantity = request.POST.get('quantity')
    cart = request.session.get('cart', {})
    if item_id in cart:
        try:
            cart[item_id]['quantity'] = int(quantity)
        except (ValueError, TypeError):
            cart[item_id]['quantity'] = 1
    request.session['cart'] = cart

    # Calculate updated values for AJAX response
    cart_items = []
    cart_subtotal = 0
    item_subtotal = 0
    for pid, item in cart.items():
        try:
            q = int(item['quantity'])
        except (ValueError, TypeError):
            q = 1
        subtotal = float(item['price']) * q
        if pid == item_id:
            item_subtotal = int(subtotal)
        cart_items.append({'id': pid, 'subtotal': subtotal})
        cart_subtotal += subtotal
    cart_discount = 250 if cart_items else 0
    cart_total = cart_subtotal - cart_discount

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'item_subtotal': item_subtotal,
            'cart_subtotal': int(cart_subtotal),
            'cart_total': int(cart_total) if cart_total > 0 else 0,
        })
    return redirect('cart')

@require_POST
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if item_id in cart:
        del cart[item_id]
    request.session['cart'] = cart
    return redirect('cart')

@require_POST
def apply_coupon(request):
    # For demo, just redirect back (discount is static)
    return redirect('cart')

def checkout_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_subtotal = 0
    for pid, item in cart.items():
        try:
            quantity = int(item['quantity'])
        except (ValueError, TypeError):
            quantity = 1
        subtotal = float(item['price']) * quantity
        cart_items.append({
            'id': pid,
            'name': item['name'],
            'price': item['price'],
            'quantity': quantity,
            'image_url': item['image'],
            'subtotal': subtotal,
        })
        cart_subtotal += subtotal
    cart_discount = 250 if cart_items else 0
    cart_total = cart_subtotal - cart_discount
    if request.method == 'POST':
        # Save order, clear cart, redirect to order complete
        request.session['cart'] = {}
        return redirect(reverse('order_complete') + '?order_id=OCD' + str(uuid.uuid4())[:6])
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'cart_subtotal': int(cart_subtotal),
        'cart_discount': cart_discount,
        'cart_total': int(cart_total) if cart_total > 0 else 0,
    })

def order_complete_view(request):
    order_id = request.GET.get('order_id', 'OCD1232')
    return render(request, 'order_complete.html', {'order_id': order_id})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'login_signup.html', {'form': form, 'signup': True})

@login_required(login_url='login')
def home_view(request):
    return render(request, 'home.html')
