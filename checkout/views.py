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
        # Always treat user as guest for now
        form = GuestEmailForm(request.POST)
        if form.is_valid():
            guest_email = form.cleaned_data['email']
            order = CheckoutOrder.objects.create(
                guest_email=guest_email,
                total_amount=total
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
            return redirect('checkout:order_success')
    else:
        form = GuestEmailForm()

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
    
def order_success(request):
    return render(request, 'checkout/order_success.html')