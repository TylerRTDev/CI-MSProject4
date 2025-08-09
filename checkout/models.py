from django.db import models
import random
from django.contrib.auth.models import User
from products.models import Product

class CheckoutOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.CharField(max_length=5, unique=True, blank=True, null=True)
    guest_email = models.EmailField(blank=True, null=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    shipping_city = models.CharField(max_length=50, null=True, blank=True)
    shipping_postcode = models.CharField(max_length=20, null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    billing_city = models.CharField(max_length=20,null=True, blank=True)
    billing_postcode = models.CharField(max_length=20,null=True, blank=True)
    stripe_session_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        while True:
            number = str(random.randint(10000, 99999))
            if not CheckoutOrder.objects.filter(order_number=number).exists():
                return number
    
    def __str__(self):
        return f"Order #{self.order_number} - {self.full_name}"

class CheckoutItem(models.Model):
    order = models.ForeignKey(CheckoutOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    size = models.CharField(max_length=10, blank=True, null=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_subtotal(self):
        return self.quantity * self.price
