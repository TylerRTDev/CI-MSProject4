from django.shortcuts import render
from products.models import Product, Genre, MediaType

def home(request):
    genres = Genre.objects.all()
    media_types = MediaType.objects.all()
    featured_clothing = Product.objects.filter(is_featured=True, category=2)[:4]
    featured_music = Product.objects.filter(is_featured=True, media_type__in=range(1, 7))[:4]
    
    return render(request, 'core/home.html', {
        'genres': genres,
        'media_types': media_types,
        'featured_clothing': featured_clothing,
        'featured_music': featured_music,
    })

def custom_404_view(request, exception):
    return render(request, 'core/404.html', status=404)