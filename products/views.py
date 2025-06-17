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
