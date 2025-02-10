from django.contrib import admin
import admin_thumbnails

from stories.models import (
    Category,Brand,Product,ProductImages,Color,Size,Variants,Slider,Banner,Future,Review
)
# Register your models here. 
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    show_change_link = True
    list_display = ['id', 'parent', 'title', 'keyword', 'description', 'image_tag', 'status', 'created_date', 'updated_date']
    list_editable = ['parent',  'status']
admin.site.register(Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    show_change_link = True
    list_display = ['id', 'title', 'keyword', 'description', 'image_tag', 'status', 'created_date', 'updated_date']
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

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin,ProductVariantsInline,]
    list_display = ['id', 'category', 'brand', 'variant', 'title', 'in_stock_max', 'in_stock_min', 'price', 'old_price', 'discount', 'is_active', 'deals', 'new_collection', 'sides_product', 'latest_collection', 'pick_collection', 'girls_collection', 'men_collection', 'pc_or_laps',  'in_stock', 'status', 'created_date', 'updated_date']
    list_editable = ['category', 'brand', 'variant', 'is_active', 'deals', 'new_collection', 'sides_product', 'latest_collection', 'pick_collection', 'girls_collection', 'men_collection', 'pc_or_laps',  'in_stock', 'status']
admin.site.register(Product, ProductAdmin)

class ProductsImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'title', 'gallery', 'image_tag', 'created_date', 'updated_date']
admin.site.register(ProductImages, ProductsImagesAdmin)

class VariantsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'title','color','size','price','quantity','image_tag']
admin.site.register(Variants, VariantsAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display = ['title','code','color_tag']
admin.site.register(Color,ColorAdmin)

class SizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'code']
admin.site.register(Size,SizeAdmin)

class SliderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'title', 'image_tag', 'created_date', 'updated_date']
    
admin.site.register(Slider, SliderAdmin)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'title', 'image_tag', 'side_deals', 'status', 'created_date', 'updated_date']
    list_editable = ['side_deals', 'status']
    
admin.site.register(Banner, BannerAdmin)

class FutureAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'title', 'hard_disk', 'cpu', 'ram', 'os', 'special_feature',  'ghaphic',  'status', 'created_date', 'updated_date']
    
admin.site.register(Future, FutureAdmin)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'subject','comment', 'rate', 'status','created_date']
    list_editable = ['status']
    readonly_fields = ['id', 'product', 'user', 'subject','comment', 'rate', 'status','created_date']
admin.site.register(Review, ReviewAdmin)