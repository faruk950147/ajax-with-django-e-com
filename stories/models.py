from django.db import models
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone

from django.db.models import Avg, Count
User = get_user_model()


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True,blank=True)
    title = models.CharField(max_length=150, unique=True, null=False, blank=False)
    keyword = models.CharField(max_length=150, unique=True, null=True, blank=True)
    description = models.CharField(max_length=150, unique=True, null=True, blank=True)
    cat_image = models.ImageField(upload_to='category', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '01. Categories'
        
    @property
    def image_tag(self):   
        if self.cat_image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.cat_image.url))
        else:
            return ""

    def __str__(self):
        return f'{self.title}'

class Brand(models.Model):
    title = models.CharField(max_length=150, unique=True, null=False, blank=False)
    keyword = models.CharField(max_length=150, unique=True, null=True, blank=True)
    description = models.CharField(max_length=150, unique=True, null=True, blank=True)
    bra_image = models.ImageField(upload_to='brand', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '02. Brands'
        
    @property
    def image_tag(self):   
        if self.bra_image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.bra_image.url))
        else:
            return ""

    def __str__(self):
        return f'{self.title}'

class Product(models.Model):
    VARIANTS = (
        ('NONE', 'NONE'),
        ('SIZES', 'SIZES'),
        ('COLORS', 'COLORS'),
        ('SIZES-COLORS', 'SIZES-COLORS'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat_products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name='bra_products')
    variant = models.CharField(max_length=12, choices=VARIANTS, default='NONE')
    title = models.CharField(max_length=150, unique=True, null=False, blank=False)
    model_title = models.CharField(max_length=150, null=True, blank=True)
    available_in_stock_msg = models.CharField(max_length=150, null=True, blank=True)
    in_stock_max = models.PositiveIntegerField(default=1)
    in_stock_min = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
    old_price = models.PositiveIntegerField(default=0)
    discount_title = models.CharField(max_length=150, null=True, blank=True)
    discount = models.PositiveIntegerField(default=0)
    # Time of the off_time field
    offers_deadline  = models.DateTimeField(auto_now_add=False, blank=True, null=True)  
    keyword = models.TextField(default='N/A')
    description = models.TextField(default='N/A')
    addition_des = models.TextField(default='N/A')
    return_policy = models.TextField(default='N/A')
    is_active = models.BooleanField(default=False)
    deals = models.BooleanField(default=False)
    new_collection = models.BooleanField(default=False)
    sides_product = models.BooleanField(default=False)
    latest_collection = models.BooleanField(default=False)
    pick_collection = models.BooleanField(default=False)
    girls_collection = models.BooleanField(default=False)
    men_collection = models.BooleanField(default=False)
    pc_or_laps = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '03. Products'
        
    @property 
    def is_offers_deadline_active(self):
        return self.offers_deadline and self.offers_deadline > timezone.now()
    @property
    def time_remaining(self):
        """Returns the remaining time in seconds."""
        if self.offers_deadline:
            return (self.offers_deadline - timezone.now()).total_seconds()
        return None

    @property
    def discount_price(self):
        if self.discount:
            discount_price = self.price - ((self.discount / 100) * self.price)
            return discount_price
        else:
            return self.price
        
    @property
    def avaregereview(self):
        reviews = Review.objects.filter(product=self, status=True).aggregate(avarage=Avg('rate'))
        avg=0
        if reviews["avarage"] is not None:
            avg=float(reviews["avarage"])
        return avg
    
    @property
    def countreview(self):
        reviews = Review.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt
        

    def __str__(self):
        return f'{self.title}'
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_images')
    title = models.CharField(max_length=50, null=True, blank=True)
    gallery = models.ImageField(upload_to='product', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '04. Products Images'
        
    @property
    def image_tag(self):   
        if self.gallery:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.gallery.url))
        else:
            return ""
 
    def __str__(self):
        return f'{str(self.product.title)}'
    
class Color(models.Model):
    title = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '05.Products Colorized'
        
    def __str__(self):
        return self.code
    @property
    def color_tag(self):
        if self.code:
            return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.code))
        else:
            return ""

class Size(models.Model):
    title = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)    

    class Meta:
        ordering = ['-id']
        verbose_name_plural = '06. Products Sizes'
        
    def __str__(self):
        return self.title

class Variants(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variants')
    title = models.CharField(max_length=100, blank=True,null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id =  models.UUIDField(primary_key=False, editable=False, default=uuid.uuid4)
    quantity = models.IntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)    

    class Meta:
        ordering = ['-id']
        verbose_name_plural = '07. Products Variations'
        
    def __str__(self):
        return self.title
    @property
    def image(self):
        img = ProductImages.objects.get(id=self.image_id)
        if img.id:
             varimage=img.gallery.url
        else:
            varimage=""
        return varimage
    @property
    def image_tag(self):
        img = ProductImages.objects.get(id=self.image_id)
        if img.id:
             return mark_safe('<img src="%s" width="50" height="50"/>' % (self.gallery.url))
        else:
            return ""

class  Slider(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='top_sliders')
    title = models.CharField(max_length=150, null=False, blank=False)
    slider_image = models.ImageField(upload_to='slider', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '08. Sliders'
        
    @property
    def image_tag(self):   
        if self.slider_image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.slider_image.url))
        else:
            return ""

    def __str__(self):
        return f'{self.title}'
    
class  Banner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=False, blank=False)
    banner_image = models.ImageField(upload_to='banners', null=True, blank=True)
    side_deals = models.BooleanField(default=False)
    new_side = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '09. Banners'
        
    @property
    def image_tag(self):   
        if self.banner_image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.banner_image.url))
        else:
            return ""

    def __str__(self):
        return f'{self.title}'
     
class  Future(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='computers')
    title = models.CharField(max_length=150, null=True, blank=True)
    hard_disk = models.CharField(max_length=150, null=True, blank=True)
    cpu = models.CharField(max_length=150, null=True, blank=True)
    ram = models.CharField(max_length=150, null=True, blank=True)
    os = models.CharField(max_length=150, null=True, blank=True)
    special_feature = models.CharField(max_length=150, null=True, blank=True)
    ghaphic = models.CharField(max_length=150, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '10. Future'
        
    def __str__(self):
        return self.title
    
class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=50,blank=True)
    rate = models.IntegerField(default=1)
    status=models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = '11. Reviews'
        
    def __str__(self):
        return self.subject