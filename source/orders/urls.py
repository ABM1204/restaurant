from django.urls import path
from orders.views import order_create, order_list, order_delete, order_update, revenue_view

urlpatterns = [
    path('', order_list, name='order_list'),
    path('create/', order_create, name='order_create'),
    path('delete/<int:id>/', order_delete, name='order_delete'),
    path('update/<int:id>', order_update, name='order_update'),
    path('revenue/', revenue_view, name='revenue'),
]
