from django.contrib import admin
from unfold.admin import ModelAdmin
import admin_thumbnails

from stories.models import (
    Category,Brand,Product,ProductImages,Color,Size,Variants,Slider,Banner,Future,Review
)
# Register your models here.
class CategoryAdmin(ModelAdmin):
    show_change_link = True
    list_display = ['id', 'parent', 'title', 'keyword', 'description', 'image_tag', 'status', 'created_date', 'updated_date']
    list_editable = ['parent',  'status']
    search_fields = ['title', 'keyword', 'description']
    list_filter = ['parent', 'status']
admin.site.register(Category, CategoryAdmin)

class BrandAdmin(ModelAdmin):
    show_change_link = True
    list_display = ['id', 'title', 'keyword', 'description', 'image_tag', 'status', 'created_date', 'updated_date']
    search_fields = ['title', 'keyword', 'description']
    list_filter = ['status', 'created_date', 'updated_date', 'title']
    readonly_fields = ['id', 'title', 'keyword', 'description', 'image_tag', 'status', 'created_date', 'updated_date']
    list_editable = ['status']
admin.site.register(Brand, BrandAdmin)

@admin_thumbnails.thumbnail('gallery')
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    readonly_fields = ('id'),
    extra = 1
    
class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True

class ProductAdmin(ModelAdmin):
    inlines = [ProductImagesAdmin,ProductVariantsInline,]
    list_display = ['id', 'category', 'brand', 'variant', 'title', 'in_stock_max', 'in_stock_min', 'price', 'old_price', 'discount',
                    'is_active', 'deals', 'new_collection', 'sides_product', 'latest_collection', 'pick_collection', 'girls_collection', 
                    'men_collection', 'pc_or_laps',  'in_stock', 'status', 'created_date', 'updated_date']
    list_editable = ['category', 'brand', 'variant', 'is_active', 'deals', 'new_collection', 'sides_product', 'latest_collection', 
                     'pick_collection', 'girls_collection', 'men_collection', 'pc_or_laps',  'in_stock', 'status']
    search_fields = ['title', 'description', 'meta_title', 'meta_description', 'meta_keyword']
    list_filter = ['category', 'brand', 'variant', 'is_active', 'deals', 'new_collection', 'sides_product', 'latest_collection', 
                   'pick_collection',]
    readonly_fields = ['id', 'category', 'brand', 'variant', 'title', 'description',
                       'in_stock_max', 'in_stock_min', 'price', 'old_price', 'discount', 'is_active', 'deals', 'new_collection', 
                       'sides_product', 'latest_collection', 'pick_collection']
admin.site.register(Product, ProductAdmin)

class ProductsImagesAdmin(ModelAdmin):
    list_display = ['id', 'product', 'title', 'gallery', 'image_tag', 'created_date', 'updated_date']
    list_editable = ['title', 'gallery']
    search_fields = ['title', 'gallery']
    list_filter = ['product', 'created_date', 'updated_date']
    readonly_fields = ['id', 'product', 'title', 'gallery', 'image_tag', 'created_date', 'updated_date']
admin.site.register(ProductImages, ProductsImagesAdmin)

class VariantsAdmin(ModelAdmin):
    list_display = ['id', 'product', 'title','color','size','price','quantity','image_tag']
    list_editable = ['title','color','size','price','quantity']
    search_fields = ['title','color','size','price','quantity']
    list_filter = ['product','color','size']
    readonly_fields = ['id', 'product', 'title','color','size','price','quantity','image_tag']
admin.site.register(Variants, VariantsAdmin)

class ColorAdmin(ModelAdmin):
    list_display = ['title','code','color_tag']
    list_editable = ['code']
    search_fields = ['title','code']
    list_filter = ['title','code']
    readonly_fields = ['color_tag']
admin.site.register(Color,ColorAdmin)

class SizeAdmin(ModelAdmin):
    list_display = ['id', 'title', 'code']
    list_editable = ['code']
    search_fields = ['title', 'code']
    list_filter = ['title', 'code']
    readonly_fields = ['id', 'title', 'code']
admin.site.register(Size,SizeAdmin)

class SliderAdmin(ModelAdmin):
    list_display = ['id', 'product', 'title', 'image_tag', 'created_date', 'updated_date']
    list_editable = ['title']
    search_fields = ['title']
    list_filter = ['product', 'created_date', 'updated_date']
    readonly_fields = ['id', 'product', 'title', 'image_tag', 'created_date', 'updated_date']
admin.site.register(Slider, SliderAdmin)
class BannerAdmin(ModelAdmin):
    list_display = ['id', 'product', 'title', 'image_tag', 'side_deals', 'status', 'created_date', 'updated_date']
    list_editable = ['side_deals', 'status']
    search_fields = ['title']
    list_filter = ['product', 'side_deals', 'status', 'created_date', 'updated_date']
    readonly_fields = ['id', 'product', 'title', 'image_tag', 'created_date', 'updated_date']
admin.site.register(Banner, BannerAdmin)

class FutureAdmin(ModelAdmin):
    list_display = ['id', 'product', 'title', 'hard_disk', 'cpu', 'ram', 'os', 'special_feature',  'ghaphic',  'status', 'created_date', 'updated_date']
    readonly_fields = ['id', 'product', 'title', 'hard_disk', 'cpu', 'ram', 'os', 'special_feature',  'ghaphic',  'status', 'created_date', 'updated_date']
    search_fields = ['title', 'hard_disk', 'cpu', 'ram', 'os', 'special_feature',  'ghaphic']
    list_filter = ['product', 'status', 'created_date', 'updated_date']
admin.site.register(Future, FutureAdmin)
class ReviewAdmin(ModelAdmin):
    list_display = ['id', 'product', 'user', 'subject','comment', 'rate', 'status','created_date']
    list_editable = ['status']
    readonly_fields = ['id', 'product', 'user', 'subject','comment', 'rate', 'status','created_date']
admin.site.register(Review, ReviewAdmin)