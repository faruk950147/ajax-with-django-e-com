from django.urls import path
from cart.views import (
    AddTtoCart, CartView
)
urlpatterns = [
    path('addtocart/<int:id>', AddTtoCart.as_view(), name='addtocart'),
    path('cartview/', CartView.as_view(), name='cartview'),
]
