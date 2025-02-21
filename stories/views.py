from ast import Try
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
import json
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
        if request.user.is_authenticated:
            context = {
                'sliders': Slider.objects.filter(status=True).order_by('id'),
                'banners': Banner.objects.filter(status=True).order_by('id')[:3],
                'side_deals_banners': Banner.objects.filter(status=False, side_deals=True).order_by('id')[:1],
                'deals_products': Product.objects.filter(offers_deadline__isnull=False,  is_active=True, deals=True, status=True).order_by("id")[:6],
                'current_time': timezone.now(),
                'new_collections': Product.objects.filter(status=True, new_collection=True).order_by('id')[:4], 
                'girls_collections': Product.objects.filter(status=True, girls_collection=True).order_by('id')[:4],
                'men_collections': Product.objects.filter(status=True, men_collection=True).order_by('id')[:4],
                'latest_collections': Product.objects.filter(status=True, latest_collection=True).order_by('id')[:4],
                'pick_collections': Product.objects.filter(status=True, pick_collection=True).order_by('id')[:4],  
            }
            return render(request, 'stories/home.html', context)
        else:
            return redirect('sign')
    
@method_decorator(never_cache, name='dispatch')    
class SingleProductView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign')
    def get(self, request, id):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=id)
            related_products = Product.objects.filter(category=product.category).exclude(id=id).order_by('-id')[:4]
            reviews = Review.objects.filter(product=product, status=True)
            reviews_total = Review.objects.filter(product=product, status=True).count()
            
            context = {
                'product': product,
                'related_products': related_products,
                'reviews': reviews,
                'reviews_total': reviews_total,
                # 'cart_form': CartForm
            }
            return render(request, 'stories/single.html', context)
        else:
            return redirect('sign')

@method_decorator(never_cache, name='dispatch')
class ReviewsView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign')
    def post(self, request):  
        if request.user.is_authenticated: 
            if request.method == "POST":
                try:
                    data = json.loads(request.body)
                    # Check if updating an existing review
                    review_id = data.get("review_id")  
                    # Get product ID from request
                    product_id = data.get("product_id")  
                    # Get the form data
                    subject = data.get("subject")
                    comment = data.get("comment")
                    rate = int(data.get("rate"))
                    product = get_object_or_404(Product, id=product_id)  # Ensure product exists
                    if review_id:  # Editing an existing review
                        review = get_object_or_404(Review, id=review_id, user_id=request.user.id)
                        review.subject = subject
                        review.comment = comment
                        review.rate = rate
                        review.save()
                    else:  # Creating a new review
                        review = Review()
                        review.product = product
                        review.user_id = request.user.id
                        review.subject = subject
                        review.comment = comment
                        review.rate = rate
                        review.save()
                    return JsonResponse({
                        "status": 200,
                        "review_id": review.id,
                        "product_id": review.product.id,
                        "user": review.user.username,
                        "subject": review.subject,
                        "comment": review.comment,
                        "rate": review.rate,  
                        "updated_date": review.updated_date.strftime('%Y-%m-%d %H:%M:%S'),
                        "messages": "Review added successfully"
                    })
                except Review.DoesNotExist:
                    return JsonResponse({"stsatus": 404, "messages": "Review not found for this user"})
        else:
            return redirect('sign')
