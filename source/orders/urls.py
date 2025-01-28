from django.urls import path
from orders.views import order_create, order_list, order_delete

urlpatterns = [
    path('', order_list, name='order_list'),
    path('create/', order_create, name='order_create'),
    path('delete/<int:id>/', order_delete, name='order_delete'),
]
