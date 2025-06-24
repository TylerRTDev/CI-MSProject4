from django.urls import path, include
from .views import checkout_view
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', checkout_view, name='checkout'),
    path('success/', views.order_success, name='order_success'),

]
