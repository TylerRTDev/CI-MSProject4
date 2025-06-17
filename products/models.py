from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)

class MediaType(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    media_type = models.ForeignKey(MediaType, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_featured = models.BooleanField(default=False)
    is_limited_edition = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)
