import uuid

from django.db import models

class Order(models.Model):
    STATUS = [
        ('в ожидании', 'В ожидании'),
        ('готово', 'Готово'),
        ('оплачено', 'Оплачено'),
    ]

    table_number = models.IntegerField()
    status = models.CharField(choices=STATUS, max_length=20, default='в ожидании')
    total_price = models.DecimalField(decimal_places=2, max_digits=10)

    def get_total_price(self):
        total = sum(item.price * item.quantity for item in self.orderitem_set.all())
        self.total_price = total
        self.save()
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField()

    def get_total_price(self):
        return self.price * self.quantity