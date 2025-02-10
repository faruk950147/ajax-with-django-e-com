from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from cart.views import (
    AddTtoCart, CartView, Quantity_inc_dec
)
urlpatterns = [
    path('addtocart/<int:id>', AddTtoCart.as_view(), name='addtocart'),
    path('cartview/', CartView.as_view(), name='cartview'),
    path("qtyincdec/", Quantity_inc_dec.as_view(), name="qtyincdec"),
]
