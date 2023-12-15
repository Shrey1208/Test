from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

class Order(models.Model):
    order_number = models.CharField(max_length=10, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField()
    address = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.order_by('-id').first()
            if last_order:
                last_number = int(last_order.order_number[3:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.order_number = f'ORD{new_number:05d}'

        super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
