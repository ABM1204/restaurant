from django.urls import path
from api_v1.views import OrderList, OrderCreate, OrderDeleteApiView, OrderUpdateApiView, RevenueApiView


urlpatterns = [
    path('order_list/', OrderList.as_view(), name='order_list_api'),
    path('order_create/', OrderCreate.as_view(), name='order_create_api'),
    path('order_delete/<int:id>/', OrderDeleteApiView.as_view(), name='order_delete_api'),
    path('order_update/<int:id>/', OrderUpdateApiView.as_view(), name='api_order_update'),
    path('revenue/', RevenueApiView.as_view(), name='api_revenue'),
]

