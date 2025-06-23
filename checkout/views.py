from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .forms import OrderForm, GuestEmailForm
from .models import CheckoutOrder, CheckoutItem
from products.models import Product

def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('products:list')

    total = sum(item['quantity'] * item['price'] for item in cart.values())

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total
            
            if request.user.is_authenticated:
                order.user = request.user
            else:
                guest_email = request.POST.get('email')
                try:
                    validate_email(guest_email)
                    order.guest_email = guest_email
                except ValidationError:
                    messages.error(request, "Please enter a valid email for guest checkout.")
                    return redirect('checkout:checkout_view')

            order.save()

            for item in cart.values():
                product = Product.objects.get(id=item['product_id'])

                # Prevent overselling
                if product.stock < item['quantity']:
                    messages.error(request, f"Not enough stock for {product.name}.")
                    order.delete()  # Cleanup
                    return redirect('cart:view_cart')

                CheckoutItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price']
                )

                product.stock -= item['quantity']
                product.save()

            request.session['cart'] = {}
            request.session.modified = True
            messages.success(request, "Order placed successfully!")
            return redirect('core:home')
    else:
        initial_data = {
            'total_amount': total,
        }
        if request.user.is_authenticated:
            initial_data['user'] = request.user

        form = OrderForm(initial=initial_data)

    return render(request, 'checkout/checkout.html', {
        'form': form,
        'cart': cart,
        'total': total,
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