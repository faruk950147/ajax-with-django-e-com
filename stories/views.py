from django.shortcuts import render,redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.db.models import Min, Max

from stories.models import (
    Category,Brand,Product,ProductImages,Color,Size,Variants,Slider,Banner,Future,Review
)
from cart.forms import CartForm
#import store models

# Create your views here.
@method_decorator(never_cache, name='dispatch')
class HomeView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign')
    def get(self, request):

        context = {
            'slider': Slider.objects.filter(status=True).order_by('id'),
            'banner': Banner.objects.filter(status=True).order_by('id')[:3],
            'side_deals_banner': Banner.objects.filter(status=True, side_deals=True).order_by('id')[:1],
            'deals_product': Product.objects.filter(offers_deadline__isnull=False,  is_active=True, deals=True, status=True).order_by("id")[:6],
            'current_time': timezone.now(),
            'new_collection': Product.objects.filter(status=True, new_collection=True).order_by('id')[:4], 
            'girls_collection': Product.objects.filter(status=True, girls_collection=True).order_by('id')[:4],
            'men_collection': Product.objects.filter(status=True, men_collection=True).order_by('id')[:4],
            'latest_collection': Product.objects.filter(status=True, latest_collection=True).order_by('id')[:4],
            'pick_collection': Product.objects.filter(status=True, pick_collection=True).order_by('id')[:4],  
        }
        return render(request, 'stories/home.html', context)
    
@method_decorator(never_cache, name='dispatch')    
class SingleProductView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        related_products = Product.objects.filter(category=product.category).exclude(id=id).order_by('-id')[:4]
        reviews = Review.objects.filter(product=product, status=True)
        reviews_total = Review.objects.filter(product=product, status=True).count()
        
        #comment checking 
        new_added = True
        checking_reviews = Review.objects.filter(user=request.user, product=product).count()
        if checking_reviews > 0:
            new_added = False
        context = {
            'product': product,
            'related_products': related_products,
            'reviews': reviews,
            'new_added': new_added,
            'reviews_total': reviews_total,
            # 'cart_form': CartForm
        }
        return render(request, 'stories/single.html', context)

@method_decorator(never_cache, name='dispatch')    
class ReviewsView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')
    def post(self, request, id):
        if request.method == "POST" or request.method == "post" and request.is_ajax():
            product = get_object_or_404(Product, id=id)
            
            review = Review()
            review.product = product
            review.user = request.user
            review.subject = request.POST.get('subject')
            review.comment = request.POST.get('comment')
            review.rate = request.POST.get('rate')
            review.save()
            return JsonResponse({
                'status': 1,
                'id': review.id,
                'user': review.user.username,
                'subject': review.subject,
                'comment': review.comment,
                'rate': review.rate,
                'created_date': review.created_date.strftime("%Y-%m-%d %H:%M:%S"),
                'messages': 'Review added successfully'
            })
            
        else:
            return HttpResponse('Something is happen')