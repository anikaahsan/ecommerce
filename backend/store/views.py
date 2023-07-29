from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin
from django.shortcuts import get_object_or_404

from store.models import Product,Collection,OrderItem,Review,Cart,CartItem
from store.serializers import ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer


class ProductViewSet(ModelViewSet):
     queryset=Product.objects.all()
     serializer_class=ProductSerializer

     def destroy(self, request, *args, **kwargs):
       
        if OrderItem.objects.filter(product__id=kwargs['pk']).count()>0:
            return Response('product cannot be deleted as it is associated with order item',
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
          
        return super().destroy(request, *args, **kwargs)
    


class CollectionViewSet(ModelViewSet): 
     queryset=Collection.objects.all()
     serializer_class=CollectionSerializer

     def destroy(self, request, *args, **kwargs):
      
        if Product.objects.filter(collection__id=kwargs['pk']).count()>0:
           return Response('collection cannot be deleted as it has product',
                              status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    
    serializer_class=ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product__id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk'] }


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet,):

    queryset=Cart.objects.prefetch_related('cartitem__product').all()
    serializer_class=CartSerializer


class CartItemViewSet(ModelViewSet):
#   queryset=CartItem.objects.all() ##shows all cartitem of all carts
#   serializer_class=CartItemSerializer

  http_method_names=['get','post','patch','delete']

  def get_queryset(self):
      return CartItem.objects.select_related('product').filter(cart__id=self.kwargs['cart_pk'])
    

  def get_serializer_class(self):
      if self.request.method=='POST':
          return AddCartItemSerializer
      if self.request.method=='PATCH':
          return UpdateCartItemSerializer
      return CartItemSerializer
  
  def get_serializer_context(self):
      return {'cart_id':self.kwargs['cart_pk']} # we get the url parameter using kwargs












