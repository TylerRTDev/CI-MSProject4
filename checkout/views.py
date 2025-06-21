from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
from .models import CheckoutOrder, CheckoutItem
from products.models import Product

@login_required
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
        form = OrderForm(initial={
            'user': request.user,
            'total_amount': total,
        })

    return render(request, 'checkout/checkout.html', {
        'form': form,
        'cart': cart,
        'total': total,
    })
