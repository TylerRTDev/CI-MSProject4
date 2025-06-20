from django.shortcuts import render

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
