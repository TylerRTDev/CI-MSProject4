from django.shortcuts import render
from django.shortcuts import redirect
from decimal import Decimal
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from products.models import Product
from django.contrib import messages


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for key, item in cart.items():
        price = Decimal(item['price'])
        quantity = item['quantity']
        subtotal = quantity * price
        total += subtotal
        
        cart_items.append({
            'id': key,
            'name': item['name'],
            'size': item.get('size', None),
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'cart/cart.html', context)

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart:view_cart')

@require_POST
def update_cart_quantity(request):
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', {})

    if item_id in cart:
        # Extract base product_id in case item_id includes size (e.g., "42_M")
        product_id = cart[item_id].get('product_id', item_id)
        product = get_object_or_404(Product, id=product_id)
        
        if quantity > product.stock:
            messages.error(request, f"Only {product.stock} units of {product.name} available in stock. Please adjust your quantity.")
            return redirect('cart:view_cart')
        
        if quantity > 0:
            cart[item_id]['quantity'] = quantity
        else:
            del cart[item_id]

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart:view_cart')

@require_POST
def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('cart:view_cart')