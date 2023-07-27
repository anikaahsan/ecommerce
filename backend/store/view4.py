from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from store.models import Product,Collection
from store.serializers import ProductSerializer,CollectionSerializer



class ProductList(APIView):

    def get(self,request):
        queryset=Product.objects.select_related('collection').all()
        serializer=ProductSerializer(queryset,many=True,) 
        return Response(serializer.data)

    def post(self,request):
        serializer=ProductSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
       

class ProductDetail(APIView):
    
    def get(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        serializer=ProductSerializer(product)
        return Response(serializer.data)


    def put(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        serializer=ProductSerializer(data=request.data,instance=product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    def delete(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        if product.orderitem_set.count()>0:
                return Response('product cannot be delted as it is associated with order item',status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response('deleted',status=status.HTTP_204_NO_CONTENT)


class CollectionList(APIView):
     
     def get(self,request):
        queryset=Collection.objects.all()
        serializer=CollectionSerializer(queryset,many=True)
        return Response(serializer.data)
    
     def post(self,request):
        serializer=CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class CollectionDetail(APIView):
     
     def get(self,request,pk):
          collection=get_object_or_404(Collection,pk=pk)
          serializer=CollectionSerializer(collection)
          return Response(serializer.data)
     
     def put(self,request,pk):
        collection=get_object_or_404(Collection,pk=pk)
        serializer=CollectionSerializer(data=request.data,instance=collection)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
     
     def delete(self,request,pk):
        collection=get_object_or_404(Collection,pk=pk)
        if collection.product_set.count()>0:
           return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response('deleted')












