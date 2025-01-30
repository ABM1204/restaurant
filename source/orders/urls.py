from django.urls import path
from orders.views import OrderCreateView, order_list, order_delete, order_update, revenue_view

urlpatterns = [
    path('order_list/', order_list, name='order_list'),
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order_delete/<int:id>/', order_delete, name='order_delete'),
    path('order_update/<int:id>', order_update, name='order_update'),
    path('revenue/', revenue_view, name='revenue'),
]
