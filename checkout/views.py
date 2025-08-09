import stripe
import os
from decimal import Decimal
from dotenv import load_dotenv
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .forms import OrderForm, GuestCheckoutForm, GuestEmailForm
from .models import CheckoutOrder, CheckoutItem
from products.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('products:list')

    total = sum(item['quantity'] * Decimal(item['price']) for item in cart.values())
    
    if request.method == 'POST':
        print("POST data received:", request.POST)
        form = GuestCheckoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            billing_address = data['billing_address']
            billing_city = data['billing_city']
            billing_postcode = data['billing_postcode']

            if data.get('same_as_shipping'):
                billing_address = data['shipping_address']
                billing_city = data['shipping_city']
                billing_postcode = data['shipping_postcode']
                
            request.session['checkout_data'] = {
                'guest_email': data['email'],
                'full_name': data['full_name'],
                'shipping_address': data['shipping_address'],
                'shipping_city': data['shipping_city'],
                'shipping_postcode': data['shipping_postcode'],
                'billing_address': billing_address,
                'billing_city': billing_city,
                'billing_postcode': billing_postcode,
                'cart': cart,
                'total': str(total),
            }
            
            return redirect('checkout:create_checkout_session')

    else:
        form = GuestCheckoutForm()

    return render(request, 'checkout/checkout.html', {
        'form': form,
        'cart': cart,
        'total': total,
        'stripe_secret_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

def guest_email_view(request):
    form = GuestEmailForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        request.session['guest_email'] = email  # Store in session
        messages.success(request, "Guest email accepted. Please complete checkout.")
        return redirect('checkout:checkout')
    
    return render(request, 'checkout/guest_email.html', {
        'form': form
    })
    
@csrf_exempt    
def create_checkout_session(request):
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    print(f"Session Key: {session_key}")
    
    checkout_data = request.session.get('checkout_data')
    if not checkout_data:
        return HttpResponseBadRequest("Missing checkout data")
    
    cart = request.session.get('cart', {})
    if not cart:
        return HttpResponseBadRequest("Cart is empty")

    line_items = []
    for item in cart.values():
        line_items.append({
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': item['name'],
                },
                'unit_amount': int(float(item['price']) * 100),
            },
            'quantity': item['quantity'],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/checkout/success/?session_id={CHECKOUT_SESSION_ID}'),
        cancel_url=request.build_absolute_uri('/cart/'),
        metadata={
            'session_key': session_key,
            'is_auth': '1' if request.user.is_authenticated else '0',
            'user_id': str(request.user.id) if request.user.is_authenticated else '',
            'guest_email': checkout_data.get('guest_email'),
            'full_name': checkout_data.get('full_name'),
            'shipping_address': checkout_data.get('shipping_address'),
            'shipping_city': checkout_data.get('shipping_city'),
            'shipping_postcode': checkout_data.get('shipping_postcode'),
            'billing_address': checkout_data.get('billing_address'),
            'billing_city': checkout_data.get('billing_city'),
            'billing_postcode': checkout_data.get('billing_postcode'),
        }
    )

    return JsonResponse({'id': session.id})

@csrf_exempt
def payment_view(request, order_id):
    order = get_object_or_404(CheckoutOrder, id=order_id)

    amount_cents = int(order.total_amount * 100)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': f'Order #{order.order_number}',
                },
                'unit_amount': amount_cents,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('checkout:order_success')
        ),
        cancel_url=request.build_absolute_uri(
            reverse('checkout:checkout')
        ),
        metadata={
            'order_id': order.id
        }
    )

    return redirect(session.url, code=303)
    
def order_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, "No session ID provided.")
        return redirect('checkout:checkout')
    order = CheckoutOrder.objects.filter(stripe_session_id=session_id).first()
    return render(request, 'checkout/order_success.html', {'order_id': order})

def order_confirmation(request, order_id):
    order = get_object_or_404(CheckoutOrder, id=order_id)
    return render(request, 'checkout/confirmation.html', {'order': order})
