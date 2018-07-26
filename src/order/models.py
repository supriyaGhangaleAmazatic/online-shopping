from django.db import models
from django.contrib.postgres.fields import JSONField


class Cart(models.Model):
    #user_id             = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name=None)
    is_cart_processed   = models.BooleanField()
    created_at          = models.DateTimeField()
    updated_at          = models.DateTimeField()

    class Meta:
        db_table = 'cart'
        managed  = False
        indexes = [
            models.Index(fields=['created_at', 'updated_at'], name='cart_index')
        ]

class Payment_method(models.Model):
    mode                = models.CharField(max_length=20)
    slug                = models.CharField(max_length=50)
    created_at          = models.DateTimeField()
    updated_at          = models.DateTimeField()

    class Meta:
        db_table = 'payment_method'
        managed  = False
        indexes = [
            models.Index(fields=['created_at', 'updated_at'], name='payment_method_index')
        ]


class Order(models.Model):
    payment_method_id       = models.ForeignKey(Payment_method,on_delete=models.CASCADE,related_name=None)
    cart_id                 = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name=None)
    #address_id              = models.ForeignKey(Address,on_delete=models.CASCADE,related_name=None)
    payment_info            = JSONField()
    shipping_name           = models.TextField()
    shipping_address_line   = models.TextField()
    shipping_city           = models.CharField(max_length=60)
    shipping_state          = models.CharField(max_length=60)
    shipping_pincode        = models.CharField(max_length=10)
    billing_name            = models.TextField()
    billing_address_line    = models.TextField()
    billing_city            = models.CharField(max_length=60)
    billing_state           = models.CharField(max_length=60)
    billing_pincode         = models.CharField(max_length=10)
    totoal_shipping_cost    = models.DecimalField( max_digits=19, decimal_places=2)    
    status                  = models.CharField(max_length=20)
    created_at              = models.DateTimeField()
    updated_at              = models.DateTimeField()

    class Meta:
        db_table = 'order'
        managed  = False
        indexes = [
            models.Index(fields=['created_at', 'updated_at','shipping_pincode','billing_pincode','shipping_city','shipping_state','billing_city','billing_state'], name='order_index')
        ]

class Cart_product(models.Model):
    cart_id             = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name=None)
    #product_id         = models.ForeignKey(Product,on_delete=models.CASCADE,related_name=None)
    #seller_id          = models.ForeignKey(Seller,on_delete=models.CASCADE,related_name=None)
    quantity            = models.IntegerField()
    is_order_generated  = models.BooleanField()
    created_at          = models.DateTimeField()
    updated_at          = models.DateTimeField()

    class Meta:
        db_table = 'cart_product'
        managed  = False
        indexes = [
            models.Index(fields=['created_at', 'updated_at'], name='cart_product_index')
        ]

class Lineitem(models.Model):
    order_id            = models.ForeignKey(Order,on_delete=models.CASCADE,related_name=None)
    #product_id         = models.ForeignKey(Product,on_delete=models.CASCADE,related_name=None)
    #seller_id          = models.ForeignKey(Seller,on_delete=models.CASCADE,related_name=None)
    status              = models.CharField(max_length=20)
    quantity            = models.IntegerField()
    base_price          = models.DecimalField( max_digits=19, decimal_places=2)
    discount            = models.DecimalField( max_digits=5, decimal_places=2,blank=True, null=True)
    shiping_cost        = models.DecimalField( max_digits=19, decimal_places=2,blank=True, null=True)
    selling_price       = models.DecimalField( max_digits=19, decimal_places=2)
    gift_wrap_charges   = models.DecimalField( max_digits=19, decimal_places=2,blank=True, null=True)
    created_at          = models.DateTimeField()
    updated_at          = models.DateTimeField()

    class Meta:
        db_table = 'lineitem'
        managed  = False
        indexes = [
            models.Index(fields=['created_at', 'updated_at','status'], name='lineitem_index')
        ]


class Order_log(models.Model):
    lineitem_id         = models.ForeignKey(Lineitem,on_delete=models.CASCADE,related_name=None)
    status              = models.CharField(max_length=20)
    description         = models.TextField(blank=True, null=True)
    created_at          = models.DateTimeField()
    updated_at          = models.DateTimeField()

    class Meta:
        db_table = 'order_log'
        managed  = False
        indexes = [
            models.Index(fields=['created_at', 'updated_at'], name='order_log_index')
        ]

class Shiping_details(models.Model):
    courior_name        = models.CharField(max_length=50)
    tracking_number     = models.CharField(max_length=50)
    deliverd_date       = models.DateField(blank=True, null=True)
    tracking_url         = models.TextField(blank=True, null=True)
    created_at          = models.DateTimeField()
    updated_at          = models.DateTimeField()

    class Meta:
        db_table = 'shiping_details'
        managed  = False
        indexes = [
            models.Index(fields=['created_at', 'updated_at','tracking_number','deliverd_date','courior_name'], name='shiping_details_index')
        ]

class Line_shiping_details(models.Model):
    lineitem_id         = models.ForeignKey(Lineitem,on_delete=models.CASCADE,related_name=None)
    shiping_details_id  = models.ForeignKey(Shiping_details,on_delete=models.CASCADE,related_name=None)
    quantity            = models.IntegerField()
    description         = models.TextField(blank=True, null=True)
    created_at          = models.DateTimeField()
    updated_at          = models.DateTimeField()

    class Meta:
        db_table = 'line_shiping_details'
        managed  = False
        indexes = [
            models.Index(fields=['created_at', 'updated_at'], name='line_shiping_details_index')
        ]

class Lineitem_tax(models.Model):
    lineitem_id         = models.ForeignKey(Lineitem,on_delete=models.CASCADE,related_name=None)
    tax_name            = models.CharField(max_length=20)
    discount            = models.DecimalField( max_digits=4, decimal_places=2)
    tax_amount         = models.DecimalField( max_digits=19, decimal_places=2)
    created_at          = models.DateTimeField()
    updated_at          = models.DateTimeField()

    class Meta:
        db_table = 'lineitem_tax'
        managed  = False
        indexes = [
            models.Index(fields=['created_at', 'updated_at','tax_name'], name='lineitem_tax_index')
        ]
