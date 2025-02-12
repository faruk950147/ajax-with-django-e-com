from django.contrib import admin
import admin_thumbnails

from cart.models import Cart

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'single_price', 'qty_total_price', ]
admin.site.register(Cart, CartAdmin)