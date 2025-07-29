from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Product, Genre, MediaType
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Product, Genre, MediaType, Category


# def product_list(request):
#     products = Product.objects.all()
#     genres = Genre.objects.all()
#     media_types = MediaType.objects.all()

#     return render(request, 'products/list.html', {
#         'products': products,
#         'genres': genres,
#         'media_types': media_types,
#     })

def product_list(request):
    genre_slug = request.GET.get('genre')
    media_type_id = request.GET.get('mediaId')
    category_slug = request.GET.get('category')
    media_slug = request.GET.get('media')

    products = Product.objects.all()

    if genre_slug:
        products = products.filter(genre__slug=genre_slug)

    if media_type_id:
        products = products.filter(media_type__id=media_type_id)

    if category_slug:
        products = products.filter(category__slug=category_slug)
        
    if media_slug:
        products = products.filter(media_type__slug=media_slug)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    genres = Genre.objects.all()
    media_types = MediaType.objects.all()
    categories = Category.objects.all()

    return render(request, 'products/list.html', {
        'page_obj': page_obj,
        'products': products,
        'genres': genres,
        'media_types': media_types,
        'categories': categories,
        'current_genre': genre_slug,
        'current_media': media_type_id,
        'current_media_slug': media_slug,
        'current_category': category_slug,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants = product.variants.filter(stock__gt=0)
    return render(request, 'products/detail.html', {
        'product': product, 
        'variants': variants
    })

def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size', None)  # optional

        product = get_object_or_404(Product, id=product_id)
        
        if quantity > product.stock:
            messages.error(request, f"Only {product.stock} units available for {product.name}.")
            return redirect('products:detail', slug=product.slug)

        cart = request.session.get('cart', {})

        key = f"{product_id}"
        if size:
            key = f"{product_id}_{size.lower()}"

        # Update or add to cart
        if key in cart:
            cart[key]['quantity'] += quantity
        else:
            cart[key] = {
                'product_id': product.id,
                'quantity': quantity,
                'size': size,
                'name': product.name,
                'price': float(product.price),
            }

        request.session['cart'] = cart
        request.session.modified = True
        print(f"Your Basket: {request.session['cart']}")
        # Display a success message in terminal
        messages.success(request, f"'{product.name}' has been added to your basket.")
        return redirect('products:detail', slug=product.slug)
    


