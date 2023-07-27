from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404

from store.models import Product,Collection
from store.serializers import ProductSerializer,CollectionSerializer



class ProductList(ListCreateAPIView):
    queryset=Product.objects.select_related('collection').all()
    serializer_class=ProductSerializer

    

class ProductDetail(RetrieveUpdateDestroyAPIView):

    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='id'

    def delete(self,request,id):
        product=get_object_or_404(Product,pk=id)
        
        if product.orderitem_set.count()>0:
                return Response('product cannot be delted as it is associated with order item',
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        product.delete()
        return Response('deleted',status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
     
     queryset=Collection.objects.all()
     serializer_class=CollectionSerializer
     

class CollectionDetail(RetrieveUpdateDestroyAPIView):
     
     queryset=Collection.objects.all()
     serializer_class=CollectionSerializer
     
     def delete(self,request,pk):
        collection=get_object_or_404(Collection,pk=pk)
        if collection.product_set.count()>0:
           return Response('collection cannot be deleted as it has product',
                           status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response('deleted')
















