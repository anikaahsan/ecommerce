from django.contrib import admin
from store.models import Product,Order,Customer,Collection


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title']


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    list_display=['placed_at']


@admin.register(Customer)
class ProductAdmin(admin.ModelAdmin):
    list_display=['email']


@admin.register(Collection)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title']



