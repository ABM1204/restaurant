from django.urls import path

from orders.api_views import OrderList, OrderCreate, OrderDeleteApiView, OrderUpdateApiView
from orders.views import OrderCreateView, order_list, OrderDeleteView, OrderUpdateView, revenue_view

urlpatterns = [
    path('order_list/', order_list, name='order_list'),
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order_delete/<int:id>/', OrderDeleteView.as_view(), name='order_delete'),
    path('order_update/<int:id>', OrderUpdateView.as_view(), name='order_update'),
    path('revenue/', revenue_view, name='revenue'),


    path('api/order_list/', OrderList.as_view(), name='order_list_api'),
    path('api/order_create/', OrderCreate.as_view(), name='order_create_api'),
    path('api/order_delete/<int:id>/', OrderDeleteApiView.as_view(), name='order_delete_api'),
    path('api/order_update/<int:id>/', OrderUpdateApiView.as_view(), name='api_order_update'),
]

