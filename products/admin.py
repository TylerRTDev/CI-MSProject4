from django.contrib import admin
from .models import Genre, MediaType, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'media_type', 'price', 'stock', 'is_featured', 'is_limited_edition', 'created_at')
    list_filter = ('genre', 'media_type', 'is_featured', 'is_limited_edition')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

admin.site.register(Genre)
admin.site.register(MediaType)