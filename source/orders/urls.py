from django.urls import path
from orders.views import OrderCreateView, order_list, OrderDeleteView, OrderUpdateView, RevenueView

urlpatterns = [
    path('order_list/', order_list, name='order_list'),
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order_delete/<int:id>/', OrderDeleteView.as_view(), name='order_delete'),
    path('order_update/<int:id>', OrderUpdateView.as_view(), name='order_update'),
    path('revenue/', RevenueView.as_view(), name='revenue'),
]
