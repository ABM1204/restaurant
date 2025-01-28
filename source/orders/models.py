import uuid

from django.db import models

class Order(models.Model):
    STATUS = [
        ('в ожидании', 'В ожидании'),
        ('готово', 'Готово'),
        ('оплачено', 'Оплачено'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table_number = models.IntegerField()
    status = models.CharField(choices=STATUS, max_length=20)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)

    def get_total_price(self):
        pass

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField()