from django.shortcuts import render
from .models import Product, Genre, MediaType

def product_list(request):
    products = Product.objects.all()
    genres = Genre.objects.all()
    media_types = MediaType.objects.all()

    return render(request, 'products/list.html', {
        'products': products,
        'genres': genres,
        'media_types': media_types,
    })

from .models import Product, Genre, MediaType, Category

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

    genres = Genre.objects.all()
    media_types = MediaType.objects.all()
    categories = Category.objects.all()

    return render(request, 'products/list.html', {
        'products': products,
        'genres': genres,
        'media_types': media_types,
        'categories': categories,
        'current_genre': genre_slug,
        'current_media': media_type_id,
        'current_media_slug': media_slug,
        'current_category': category_slug,
    })
