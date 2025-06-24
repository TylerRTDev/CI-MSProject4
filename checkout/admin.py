from django.contrib import admin
from .models import CheckoutOrder, CheckoutItem

from django.contrib import admin
from .models import CheckoutOrder, CheckoutItem

@admin.register(CheckoutOrder)
class CheckoutOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'user', 'guest_email', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'user__username', 'guest_email')