from django.contrib import admin
from Shop.models import Productimage,Product,Brands,Category,ProductDescription
from Shop.models import Review,ProductFeautures
# Register your models here.
class Image(admin.TabularInline):
    model = Productimage
    extra = 1 

class ProductFeaturesinline(admin.TabularInline):
    model = ProductFeautures
    extra = 1

class ProductDescriptionInline(admin.TabularInline):
    model = ProductDescription
    extra = 1

@admin.register(Product)
class admininline(admin.ModelAdmin):
    inlines = [Image,ProductDescriptionInline,ProductFeaturesinline]

admin.site.register(Brands)
admin.site.register(Category)
admin.site.register(Review)