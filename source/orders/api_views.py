from rest_framework import generics, permissions
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer

class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

from rest_framework import generics, permissions
from .models import Order
from .serializers import OrderSerializer

class OrderCreate(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        order = serializer.save()
        items_data = self.request.data.get('items', [])

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        order.update_total_price()
