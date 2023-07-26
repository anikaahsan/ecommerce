from django.db import models

class Promotion(models.Model):
     description=models.CharField(max_length=255)
     discount=models.FloatField()
 ##product_set ---> returns all the product that has a particular promotion is applied to 


class Collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product',on_delete=models.SET_NULL,related_name='+',null=True,blank=True) ## this tells the django not to create reverse relationship
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['title']

class Product(models.Model):
    # id=models.CharField(max_length=10,primary_key=True)
    title=models.CharField(max_length=255)
    description=models.TextField(null=True,blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    inventory=models.IntegerField()
    image=models.ImageField(upload_to='images',null=True,blank=True)
    last_update=models.DateTimeField(auto_now=True)

    collection=models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotions=models.ManyToManyField(Promotion,null=True,blank=True) ##related_name='products'
    
    def __str__(self):
        return self.title

class Customer(models.Model):
    membership_bronze='Bronze'
    membership_Silver='Silver'
    membership_Gold='Gold'

    membership_choices=[
        (membership_bronze,'Bronze'),
        (membership_Silver,'Silver'),
        (membership_Gold,'Gold'),
    ]

    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=11,editable=True)
    birth_date=models.DateField(null=True,blank=True)
    membership=models.CharField(max_length=10,
                                        choices=membership_choices,
                                        default=membership_bronze)
    

class address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer=models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True) ## we delete the customer the associated address will be deleted


class Order(models.Model):
    payment_status_pending='Pending'
    payment_status_complete='Complete'
    payment_status_failed='Failed'
    
    payment_status_choices=[
        (payment_status_pending,'Pending'),
         (payment_status_complete,'Pending'),
           (payment_status_failed,'Pending'),
    ]
    
    placed_at=models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=10,
                                                  choices=payment_status_choices,
                                                  default=payment_status_pending)  
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT)  
    ## a customer can have multiple orders

class OrderItem(models.Model):
    quantity=models.PositiveIntegerField() 
    unit_price=models.DecimalField(max_digits=10,decimal_places=2) 

        ## an order can have multiple order items
    order=models.ForeignKey(Order,on_delete=models.PROTECT) 
    product=models.ForeignKey(Product,on_delete=models.PROTECT) 
    


class Cart(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    quantity=models.PositiveIntegerField()
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)    

