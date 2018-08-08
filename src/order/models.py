"""
        Configuration of Modules
"""
from user import models as user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from utils.models import CustomBaseModelMixin
from seller import models as seller_model
from product import models as product_model


class Cart(CustomBaseModelMixin):
    """
        Configuration of CartModules
    """
    user = models.ForeignKey(
        user_model.User,
        on_delete=models.CASCADE,
        related_name=None)
    is_cart_processed = models.BooleanField()


class PaymentMethod(CustomBaseModelMixin):
    """
        Configuration of PaymentMethodModules
    """
    mode = models.CharField(max_length=20)
    slug = models.CharField(max_length=50, unique=True)


class Order(CustomBaseModelMixin):
    """
        Configuration of OrderModules
    """
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
        related_name=None)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name=None)
    payment_info = JSONField()
    shipping_name = models.TextField()
    shipping_address_line = models.TextField()
    shipping_city = models.CharField(max_length=60)
    shipping_state = models.CharField(max_length=60)
    shipping_pincode = models.CharField(max_length=10)
    billing_name = models.TextField()
    billing_address_line = models.TextField()
    billing_city = models.CharField(max_length=60)
    billing_state = models.CharField(max_length=60)
    billing_pincode = models.CharField(max_length=10)
    totoal_shipping_cost = models.DecimalField(max_digits=19, decimal_places=2)
    status = models.CharField(max_length=20)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'shipping_pincode',
                    'billing_pincode',
                    'shipping_city',
                    'shipping_state',
                    'billing_city',
                    'billing_state'],
                name='order_index')]


class CartProduct(CustomBaseModelMixin):
    """
        Configuration of CartProductModules
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name=None)
    product = models.ForeignKey(
        product_model.Product,
        on_delete=models.CASCADE,
        related_name=None)
    seller = models.ForeignKey(
        seller_model.Seller,
        on_delete=models.CASCADE,
        related_name=None)
    quantity = models.PositiveIntegerField()
    is_order_generated = models.BooleanField()


class Lineitem(CustomBaseModelMixin):
    """
        Configuration of LineitemModules
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name=None)
    product = models.ForeignKey(
        product_model.Product,
        on_delete=models.CASCADE,
        related_name=None)
    seller = models.ForeignKey(
        seller_model.Seller,
        on_delete=models.CASCADE,
        related_name=None)
    status = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    base_price = models.DecimalField(max_digits=19, decimal_places=2)
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True)
    shiping_cost = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True)
    selling_price = models.DecimalField(max_digits=19, decimal_places=2)
    gift_wrap_charges = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True)


class OrderLog(CustomBaseModelMixin):
    """
        Configuration of OrderLogModules
    """
    lineitem = models.ForeignKey(
        Lineitem,
        on_delete=models.CASCADE,
        related_name=None)
    status = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)


class ShippingDetails(CustomBaseModelMixin):
    """
        Configuration of ShippingDetailsModules
    """
    courior_name = models.CharField(max_length=50)
    tracking_number = models.CharField(max_length=50)
    deliverd_date = models.DateField(blank=True, null=True)
    tracking_url = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'tracking_number',
                    'deliverd_date',
                    'courior_name'],
                name='shiping_details_index')]


class LineShippingDetails(CustomBaseModelMixin):
    """
        Configuration of LineShippingDetailsModules
    """
    lineitem = models.ForeignKey(
        Lineitem,
        on_delete=models.CASCADE,
        related_name=None)
    shipping_details = models.ForeignKey(
        ShippingDetails,
        on_delete=models.CASCADE,
        related_name=None)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)


class LineitemTax(CustomBaseModelMixin):
    """
        Configuration of LineitemTaxModules
    """
    lineitem = models.ForeignKey(
        Lineitem,
        on_delete=models.CASCADE,
        related_name=None)
    tax_name = models.CharField(max_length=20)
    discount = models.DecimalField(max_digits=4, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'tax_name'],
                name='lineitem_tax_index')]
