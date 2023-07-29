from django.urls import path
from store import views

from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers
from pprint import pprint

app_name='store'

# # router=SimpleRouter()
# router=DefaultRouter()
router=routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet,basename='collections')
router.register('cart',views.CartViewSet,basename='cart')
pprint(router.urls)

#child router
products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet,basename='product_review')
pprint(products_router.urls)

#child router
cart_router=routers.NestedDefaultRouter(router,'cart',lookup='cart') #cart_pk
cart_router.register('cartitems',views.CartItemViewSet,basename='cartitems')
pprint(cart_router.urls)

urlpatterns = router.urls +products_router.urls+cart_router.urls
  

































  # path('products/',views.ProductList.as_view(),name='product_list'),
    # path('products/<int:id>',views.ProductDetail.as_view(),name='product_detail'),
    # path('collections/',views.CollectionList.as_view(),name='collection_list'),
    # path('collections/<int:pk>/',views.CollectionDetail.as_view(),name='collection_detail'),