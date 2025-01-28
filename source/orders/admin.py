from django.contrib import admin
from .models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'status', 'total_price')
    list_filter = ('status', 'total_price')
    inlines = (OrderItemInline)
