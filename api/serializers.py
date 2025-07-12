from rest_framework import serializers
from store.models import Product, Category, Cart, Order, Review,Offer
from django.contrib.auth.models import User

# -------- Category -------- #
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# -------- Product -------- #
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'slug', 'price', 'gender', 'age_group', 'image', 'category', 'category_id']

# -------- Cart -------- #
class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_id', 'user', 'created_date', 'status', 'quantity']

# -------- Order -------- #
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

# -------- Review -------- #
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'



class OfferSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'product', 'product_name', 'discount', 'isAvailable', 'start_date', 'end_date', 'discounted_price']

    def get_discounted_price(self, obj):
        return obj.discounted_price()

