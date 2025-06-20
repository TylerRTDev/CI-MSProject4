from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('remove/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/', views.update_cart_quantity, name='update_cart'),
]