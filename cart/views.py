from django.shortcuts import render,redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.db.models import Min, Max
from cart.forms import (
    CartForm
)
from stories.models import (
    Product
)
from cart.models import (
    Cart
)

# Create your views here.
@method_decorator(never_cache, name='dispatch')
class AddTtoCart(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign')
    def post(self, request, id):
        if request.user.is_authenticated:
            url = request.META.get('HTTP_REFERER')  
            cart_filter = Cart.objects.filter(product_id=id, user_id=request.user.id)
            if cart_filter:
                control = 1
            else:
                control = 0
            if request.method == "POST" or request.method == "post" and request.is_ajax():
                cartForm = CartForm(request.POST)
                if cartForm.is_valid():
                    if control == 1:
                        cartItem = get_object_or_404(Cart, product_id=id, user_id=request.user.id)
                        cartItem.quantity += int(request.POST.get('quantity'))
                        cartItem.save()
                    else:
                        cartItem = Cart()
                        cartItem.product_id = id
                        cartItem.user_id = request.user.id
                        cartItem.save()
                return HttpResponseRedirect(url)
            else:
                return HttpResponse('Get method not allowed')
        else:
            return HttpResponseRedirect(reverse_lazy('sign'))

@method_decorator(never_cache, name='dispatch')
class CartView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign')
    def get(self, request):
        if request.user.is_authenticated:
            context = {
                
            }
            return render(request, 'cart/cart.html', context)
        else:
            return HttpResponseRedirect(reverse_lazy('sign'))
    
@method_decorator(never_cache, name='dispatch')
class QuantityIncDec(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign')
    def post(self, request):
        if request.user.is_authenticated:
            if request.method == "POST" or request.method == "post" and request.is_ajax(): 
                id = request.POST.get("id")
                action = request.POST.get("action")
                try:
                    cart_product = get_object_or_404(Cart, id=id, user=request.user.id)
  
                    # Get maximum stock allowed
                    max_stock = cart_product.product.in_stock_max  

                    # Increase or decrease quantity based on action
                    if action == "increase":
                        if cart_product.quantity < max_stock:
                            cart_product.quantity += 1
                        else:
                            return JsonResponse({
                                "status": 400,
                                "messages": f"Cannot add more than {max_stock} units of this product!",
                                "quantity": cart_product.quantity
                            })
                    
                    elif action == "decrease":
                        if cart_product.quantity > 1:
                            cart_product.quantity -= 1
                        else:
                            return JsonResponse({
                                "status": 400,
                                "messages": "Quantity cannot be less than 1!",
                                "quantity": cart_product.quantity
                            })

                    cart_product.save()
                    
                    cart_products = Cart.objects.filter(user_id=request.user.id)
                    return JsonResponse({"status": 200, 
                                        "messages": f"Quantity updated successfully! {cart_product.quantity}",
                                        "quantity": cart_product.quantity,
                                        "cart_total": sum(item.quantity * item.product.price for item in cart_products),
                                        "qty_total_price": cart_product.product.price * cart_product.quantity,
                                        "sub_total": sum(item.quantity * item.product.price for item in cart_products),
                                        "finale_price": sum(item.quantity * item.product.price for item in cart_products) + 150,
                                        "id": id
                                        })
                
                except Cart.DoesNotExist:
                    return JsonResponse({"status": 401, 
                                        "messages": "Product not found"
                                        })
            return JsonResponse({"status": 402, 
                                "messages": "Something is happen"
                                })
        else:
            return JsonResponse({"status": 403, 
                                "messages": "You are not logged in !"
                                })

@method_decorator(never_cache, name='dispatch')
class RemoveToCart(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign')
    def post(self, request):
        if request.user.is_authenticated:
            if request.method == "POST" or request.method == "post" and request.is_ajax(): 
                id = request.POST.get("id")

            try:
                cart_item = get_object_or_404(Cart, id=id, user=request.user.id)
                cart_item.delete()
                
                cart_products = Cart.objects.filter(user_id=request.user.id)
                
                return JsonResponse({"status": 200,
                                     "messages": "Product removed successfully !", 
                                    "cart_total": sum(item.quantity * item.product.price for item in cart_products),
                                    "qty_total_price": cart_item.product.price * cart_item.quantity,
                                    "sub_total": sum(item.quantity * item.product.price for item in cart_products),
                                    "finale_price": sum(item.quantity * item.product.price for item in cart_products) + 150,
                                    "id": id})

            except Cart.DoesNotExist:
                return JsonResponse({"status": 400, "messages": "Product not found"})

        return JsonResponse({"status": 400, "messages": "Invalid request"})
