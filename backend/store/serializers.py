from rest_framework import serializers
from store.models import Product,Collection
from decimal import Decimal




class CollectionSerializer(serializers.ModelSerializer):

    def calculate_total_product(self,collection:Collection):
        num_of_product=collection.product_set.count()
        return num_of_product


    product_count=serializers.SerializerMethodField(method_name='calculate_total_product')

    class Meta:
        model=Collection
        fields=['id','title','product_count']



class ProductSerializer(serializers.ModelSerializer):
   
    def calculate_tax(self,product:Product):
        return product.price*Decimal(1.1)
    
    ##custom serializer field
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    
    # collection=CollectionSerializer(read_only=True)
  
   
    class Meta:
        model=Product
        fields='__all__'
      


         # collection=serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # ) ##no effect when __all__
    # collection=serializers.StringRelatedField()---->returns the title (__str__)

      # collection=serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection_detail',
        
    # ) //not working

#  def validate(self, data): ## data -->dictionary
#         if data['password']!=data['confirm_password']:
#             return serializers.ValidationError('password do not match')
#         return data

#  def create(self, validated_data): validated data dictionary
#        product=Product(**validated_data) unpacking the dictionary
#        product.other=1
#        product.save()
#        return product