from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('<slug:slug>/', views.product_detail, name='detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)