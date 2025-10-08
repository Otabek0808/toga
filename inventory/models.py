from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Mahsulot nomi')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Sotish narxi')       # sotish narxi
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tannarxi')  # tannarx
    quantity = models.PositiveIntegerField(default=0, verbose_name='Soni')                  # zaxira
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class SoldProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sold_price = models.DecimalField(max_digits=10, decimal_places=2)
    sold_at = models.DateTimeField(auto_now_add=True)

    @property
    def profit(self):
        return self.sold_price - self.product.cost_price


    def __str__(self):
        return f"{self.product.name} sotildi"
