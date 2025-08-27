import stripe
import json
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import GuestCheckoutForm, GuestEmailForm
from .models import CheckoutOrder, CheckoutItem
from products.models import Product
from django.contrib.auth import get_user_model
from decimal import Decimal

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('products:list')

    total = sum(item['quantity'] * Decimal(item['price']) for item in cart.values())
    
    form = GuestCheckoutForm()
    
    if request.method == 'POST':
        form = GuestCheckoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pass
        else:
            if request.user.is_authenticated:
                initial = {
                    'email': request.user.email,
                    'full_name': f"{request.user.first_name} {request.user.last_name}",
                }
                form = GuestCheckoutForm(initial=initial)
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


@require_POST
@csrf_exempt
def create_checkout_session(request):
    cart = request.session.get('cart', {})
    if not cart:
        return JsonResponse({'error': 'Cart is empty'}, status=400)
    
    form = GuestCheckoutForm(request.POST)
    if not form.is_valid():
        print("FORM ERRORS:", form.errors)
        return JsonResponse({'error': 'Invalid form data'}, status=400)
    
    data = form.cleaned_data

    line_items = []
    cart_with_ids = {}
    for item in cart.values():
        # item['product_id'] = product_id  # Add ID to each item
        # cart_with_ids[product_id] = item
        
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
    
    metadata = {
        'user_id': request.user.id if request.user.is_authenticated else '', # Store user ID if authenticated
        'email': request.session.get('email') or data['email'],
        'guest_full_name': data['full_name'],
        'full_name': data['full_name'],
        'shipping_address': data['shipping_address'],
        'shipping_city': data['shipping_city'],
        'shipping_postcode': data['shipping_postcode'],
        'billing_address': data['billing_address'] if not data.get('same_as_shipping') else data['shipping_address'],
        'billing_city': data['billing_city'] if not data.get('same_as_shipping') else data['shipping_city'],
        'billing_postcode': data['billing_postcode'] if not data.get('same_as_shipping') else data['shipping_postcode'],
        'cart': json.dumps(cart_with_ids),  # Store cart details as JSON string
    }
        
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('checkout:order_success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('checkout:checkout')),
            customer_email=data['email'],
            metadata=metadata,
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'id': session['id']})
    
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})

        # Prevent duplicate order creation
        if CheckoutOrder.objects.filter(order_session=session['id']).exists():
            return JsonResponse({'status': 'Order already exists'}, status=200)
        
        User = get_user_model()

        user = None
        user_id = metadata.get('user_id')
        email = metadata.get('email')
        
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                user = None

        # Create the order
        order = CheckoutOrder.objects.create(
            user=user,
            order_session=session['id'],
            email=email,
            full_name=metadata.get('full_name'),
            shipping_address=metadata.get('shipping_address'),
            shipping_city=metadata.get('shipping_city'),
            shipping_postcode=metadata.get('shipping_postcode'),
            billing_address=metadata.get('billing_address'),
            billing_city=metadata.get('billing_city'),
            billing_postcode=metadata.get('billing_postcode'),
            total_amount=session['amount_total'] / 100,
        )

        # Create order items from cart
        try:
            cart_data = json.loads(metadata.get('cart', '{}'))
            for item in cart_data.values():
                product = Product.objects.get(id=item['product_id'])
                CheckoutItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price'],
                    size=item.get('size', '')
                )
                product.stock -= item['quantity']
                product.save()
        except Exception as e:
            return JsonResponse({'error': f'Item processing failed: {str(e)}'}, status=500)

    return JsonResponse({'status': 'success'}, status=200)

def order_success(request):
    session_id = request.GET.get('session_id')
    
    if not session_id:
        return redirect('products:list')
        
    order = CheckoutOrder.objects.filter(order_session=session_id).first()
    
    if not order:
        return render(request, 'core/404.html', status=404)
    
    request.session['cart'] = {}  # Clear the cart after successful order
    request.session.modified = True  # Mark session as modified to save changes
    
    return render(request, 'checkout/order_success.html', {'order': order})

def order_confirmation(request, order_id):
    order = CheckoutOrder.objects.filter(order_session=order_id).first()
    
    if not order:
        return render(request, 'core/404.html', status=404)
    
    return render(request, 'checkout/confirmation.html', {'order': order})
