
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from store.models import Product,Collection
from store.serializers import ProductSerializer,CollectionSerializer

@api_view(['GET','POST'])
def product_list(request):
    
    if request.method=='GET':
        queryset=Product.objects.select_related('collection').all()
        serializer=ProductSerializer(queryset,many=True,) ##context={'request':request}
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=ProductSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
       


@api_view(['GET','PUT','DELETE'])
def product_detail(request,pk):
     try:
            product=Product.objects.get(pk=pk)
     except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)       

     if request.method=='GET':
            serializer=ProductSerializer(product)
            return Response(serializer.data)
      
     elif request.method=='PUT':
        
        serializer=ProductSerializer(data=request.data,instance=product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
     elif request.method=='DELETE':
      
        if product.orderitem_set.count()>0:
            return Response('product cannot be delted as it is associated with order item',status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response('deleted',status=status.HTTP_204_NO_CONTENT)

    
@api_view(['GET','POST'])
def collection_list(request):

    if request.method=="GET":
        queryset=Collection.objects.all()
        serializer=CollectionSerializer(queryset,many=True)
        return Response(serializer.data)
    
    elif request.method=='POST':
        serializer=CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




@api_view(['GET','PUT','DELETE'])
def collection_detail(request,pk):
    try:
       collection=Collection.objects.get(pk=pk)
    except Collection.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer=CollectionSerializer(collection)
        return Response(serializer.data)
    
    elif request.method=='PUT':
        serializer=CollectionSerializer(data=request.data,instance=collection)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    elif request.method=='DELETE':
        if collection.product_set.count()>0:
           return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response('deleted')

   

