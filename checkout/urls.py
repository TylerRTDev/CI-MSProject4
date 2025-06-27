from django.urls import path, include
from .views import checkout_view, order_confirmation
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', checkout_view, name='checkout'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.order_success, name='order_success'),
    path('confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
]
