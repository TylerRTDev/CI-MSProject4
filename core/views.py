from django.shortcuts import render
from products.models import Genre, MediaType, Product

def home(request):
    featured = Product.objects.filter(is_featured=True)[:4]
    genres = Genre.objects.all()
    media_types = MediaType.objects.all()
    return render(request, 'core/home.html', {
        'featured': featured,
        'genres': genres,
        'media_types': media_types,
    })