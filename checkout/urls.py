from django.urls import path, include
from .views import checkout_view

app_name = 'checkout'

urlpatterns = [
    path('', checkout_view, name='checkout'),

]
