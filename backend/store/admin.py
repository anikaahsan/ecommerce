from django.contrib import admin
from store.models import Product,Order,Customer,Collection,OrderItem,Review,Cart,CartItem


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title',]


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    list_display=['placed_at','payment_status','customer']


@admin.register(Customer)
class ProductAdmin(admin.ModelAdmin):
    list_display=['email']


@admin.register(Collection)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title',]


@admin.register(OrderItem)
class ProductAdmin(admin.ModelAdmin):
    list_display=['product','quantity','order']

@admin.register(Review)
class ProductAdmin(admin.ModelAdmin):
    list_display=['product','description','name']

@admin.register(Cart)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','created_at']


@admin.register(CartItem)
class ProductAdmin(admin.ModelAdmin):
    list_display=['product','quantity','cart']        



