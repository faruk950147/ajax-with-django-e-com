from django.db import models
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
from django.db.models import Avg, Count
User = get_user_model()
from stories.models import (
    Product,Variants
)

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, blank=True, null=True) 
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '01. Carts'
        
    @property
    def single_price(self):
        return (self.product.price)

    @property
    def qty_total_price(self):
        return (self.quantity * self.product.price)

    # @property
    # def Variants_price(self):
    #     return (self.quantity * self.variant.price)
    
    def __str__(self):
        return self.product.title