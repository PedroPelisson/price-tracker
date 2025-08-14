from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_url = models.URLField(unique=True, max_length=700)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    desired_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_update = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name