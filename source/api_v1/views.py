from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import Order, OrderItem
from api_v1.serializers import OrderSerializer


class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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


class OrderDeleteApiView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self):
        return Order.objects.get(id=self.kwargs['id'])

class OrderUpdateApiView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        return get_object_or_404(Order, id=self.kwargs['id'])


class RevenueApiView(APIView):
    def get(self, request, *args, **kwargs):
        revenue = Order.calculate_revenue()
        return Response({"revenue": revenue}, status=status.HTTP_200_OK)

