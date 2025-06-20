from django.shortcuts import render
from django.shortcuts import redirect

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for key, item in cart.items():
        subtotal = item['quantity'] * item['price']
        total += subtotal
        cart_items.append({
            'id': key,
            'name': item['name'],
            'size': item.get('size', None),
            'quantity': item['quantity'],
            'price': item['price'],
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
