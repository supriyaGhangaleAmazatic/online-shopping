"""
    serializers for product app
"""
from rest_framework import serializers, exceptions
from .models import (User,
                     Product,
                     Category,
                     Wishlist,
                     Review,
                     ProductSeller,
                     ProductFeature,
                     Feature)
from django.utils import timezone

class CategorySerializer(serializers.ModelSerializer):
    """
        serializers for product app
    """
    class Meta:
        '''meta'''
        model = Category
        fields = ('id','name','slug')

class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    base_price = serializers.SerializerMethodField()
    selling_price = serializers.SerializerMethodField()
    img = serializers.SerializerMethodField()
    in_stock = serializers.SerializerMethodField()
    feature = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id',
                  'slug',
                  'name',
                  'rating',
                  'base_price',
                  'selling_price',
                  'img',
                  'in_stock',
                  'feature',
                  'description',
                  'reviews')
    def get_rating(self,obj):
        rev = list(Review.objects.filter(product=obj).values_list('rating', flat=True))
        if rev:
            avg_ret = sum(rev) / len(rev)
        else:
            avg_ret = 0
        return avg_ret

    def get_base_price(self, obj):
        return obj.base_price
    
    def get_selling_price(self, obj):
        return obj.selling_price
    
    def get_img(self, obj):
        return obj.images

    def get_in_stock(self, obj):
        qty = list(ProductSeller.objects.filter(product=obj).values_list('quantity',flat=True))
        return sum(qty)
    
    def get_feature(self, obj):
        feature_list = Feature.objects.filter(category=obj.category)
        features = {}
        for feature_object in feature_list:
            try:
                feature_name = feature_object.name
                feature_value = ProductFeature.objects.filter(
                    feature=feature_object, product=obj).values_list('value', flat=True).get()
                features.update({feature_name : feature_value})
            except Exception:
                return ""

        return features
    
    def get_description(self, obj):
        return obj.description

    def get_reviews(self, obj):
        rev = Review.objects.filter(product=obj).values('id',
                                                        'rating',
                                                        'user',
                                                        'title',
                                                        'description')
        return rev



class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('id', 'product')

    def create(self, validate_data):
        return Wishlist.objects.create(user=self.context['request'].user, product=validate_data['product'])

class ProductSellerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    selling_price = serializers.SerializerMethodField()
    selling_exprience = serializers.SerializerMethodField()
    delivery_days = serializers.SerializerMethodField()

    class Meta:
        model = ProductSeller
        fields = ('id',
                  'name',
                  'rating',
                  'selling_price',
                  'selling_exprience',
                  'delivery_days')

    def get_name(self, obj):
        return obj.seller.company_name
    
    def get_rating(self, obj):
        rev = list(Review.objects.filter(seller=obj.seller).values_list('rating', flat=True))
        if rev:
            avg_ret = sum(rev) / len(rev)
        else:
            avg_ret = 0
        return avg_ret
    def get_selling_exprience(self, obj):
        return str(timezone.now().year - obj.created_at.year)+" years."
    def get_selling_price(self, obj):
        price = obj.product.selling_price
        discount = obj.discount
        sp = price - (price*(discount/100))
        return sp
    def get_delivery_days(self, obj):
        return {"min":obj.min_delivery_days,
                "max":obj.max_delivery_days}

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'title', 'description', 'rating')
class ReviewPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('user', 'seller', 'product', 'rating', 'title', 'description')
