import stripe
import os
from dotenv import load_dotenv
from django.conf import settings
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

    total = sum(item['quantity'] * item['price'] for item in cart.values())

    # if request.method == 'POST':
    #     form = GuestEmailForm(request.POST)
    #     if form.is_valid():
    #         guest_email = form.cleaned_data['email']
            
    #         if request.user.is_authenticated:
    #             order = CheckoutOrder.objects.create(
    #                 user=request.user,
    #                 total_amount=total
    #             )
    #         else:
    #             order = CheckoutOrder.objects.create(
    #                 guest_email=guest_email,
    #                 total_amount=total
    #             )

    #         for item in cart.values():
    #             product = Product.objects.get(id=item['product_id'])

    #             if product.stock < item['quantity']:
    #                 messages.error(request, f"Not enough stock for {product.name}.")
    #                 order.delete()
    #                 return redirect('cart:view_cart')

    #             CheckoutItem.objects.create(
    #                 order=order,
    #                 product=product,
    #                 quantity=item['quantity'],
    #                 price=item['price'],
    #                 size=item.get('size', '')
    #             )

    #             product.stock -= item['quantity']
    #             product.save()

    #         request.session['cart'] = {}
    #         request.session.modified = True
    #         messages.success(request, "Order placed successfully!")
    #         return redirect('checkout:order_confirmation', order_id=order.id)
    # else:
    #     form = GuestEmailForm()
    
    if request.method == 'POST':
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

            order = CheckoutOrder.objects.create(
                user=request.user if request.user.is_authenticated else None,
                guest_email=data['email'],
                full_name=data['full_name'],
                shipping_address=data['shipping_address'],
                shipping_city=data['shipping_city'],
                shipping_postcode=data['shipping_postcode'],
                billing_address=billing_address,
                billing_city=billing_city,
                billing_postcode=billing_postcode,
                total_amount=total,
            )

            for item in cart.values():
                product = Product.objects.get(id=item['product_id'])

                if product.stock < item['quantity']:
                    messages.error(request, f"Not enough stock for {product.name}.")
                    order.delete()
                    return redirect('cart:view_cart')

                CheckoutItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price'],
                    size=item.get('size', '')
                )

                product.stock -= item['quantity']
                product.save()

            request.session['cart'] = {}
            request.session.modified = True
            messages.success(request, "Order placed successfully!")
            return redirect('checkout:payment', order_id=order.id)
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
    
def create_checkout_session(request):
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
        success_url=request.build_absolute_uri('/checkout/success/'),
        cancel_url=request.build_absolute_uri('/cart/'),
    )

    return JsonResponse({'id': session.id})
    
def create_checkout_session(request):
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
        success_url=request.build_absolute_uri('/checkout/success/'),
        cancel_url=request.build_absolute_uri('/cart/'),
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
                'currency': 'usd',
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
    return render(request, 'checkout/order_success.html')

def order_confirmation(request, order_id):
    order = get_object_or_404(CheckoutOrder, id=order_id)
    return render(request, 'checkout/confirmation.html', {'order': order})
