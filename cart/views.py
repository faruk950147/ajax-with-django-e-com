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

@method_decorator(never_cache, name='dispatch')
class CartView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign')
    def get(self, request):
        context = {
            
        }
        return render(request, 'cart/cart.html', context)