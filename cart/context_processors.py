from django.shortcuts import redirect, get_object_or_404
from django.db.models import Min, Max
from django.utils import timezone
from cart.models import Cart
from stories.models import (
    Category, Brand, Product, ProductImages, Color, Size, Variants,
)

def get_filters(request):
    cart_products = Cart.objects.filter(user_id=request.user.id)
    cart_total_price = 0
    for cart_product in cart_products:
        cart_total_price += cart_product.product.price * cart_product.quantity
    return {
        'cart_products': cart_products,
        'cart_total_price': cart_total_price,
    }