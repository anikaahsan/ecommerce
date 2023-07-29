from rest_framework import serializers
from store.models import Product,Collection,Review,Cart,CartItem
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

class  CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','price']
              

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','date','description','name']

    def create(self, validated_data):
        product_id=self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    product=CartProductSerializer()
    total_price=serializers.SerializerMethodField(method_name='calculate_price')

    def calculate_price(self,cartitem:CartItem):
      return cartitem.product.price*cartitem.quantity

    class Meta:
        model=CartItem
        fields=['quantity','cart','product','id','total_price']   


class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    cartitem=CartItemSerializer(many=True,read_only=True)

    total_price=serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self,cart:Cart):
        return sum([ item.quantity * item.product.price for item in cart.cartitem.all()])
           
    class Meta:
        model=Cart
        fields=['id','created_at','cartitem','total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    # product_id=serializers.IntegerField()

    # def validate_product_id(self,value):
    #     if not Product.objects.filter(pk=value):
    #         raise serializers.ValidationError('no product founf with this id')
    #     return value

    def save(self, **kwargs):
        cart_id=self.context['cart_id']
        product=self.validated_data['product']
        quantity=self.validated_data['quantity']
        


        try:
           #updating a existing item 
           cartitem= CartItem.objects.get(cart_id=cart_id,product=product)
           cartitem.quantity=quantity
           cartitem.save()
           self.instance=cartitem
        except CartItem.DoesNotExist:
            #create a new item
            self.instance=CartItem.objects.create(cart_id=cart_id,**self.validated_data)    
          
        return self.instance 

  
    class Meta:
        model=CartItem
        fields= ['id','quantity','product',]   



class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']









































































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