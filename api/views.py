from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from store.models import Product, Category, Cart, Order, Review,Offer
from api.serializers import ProductSerializer, CategorySerializer,CartSerializer, OrderSerializer, ReviewSerializer,OfferSerializer



#.....CATEGORY VIEWSET....[List/create/get single category/update/delete]....#

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

#.....PRODUCT VIEWSET ....[List/create/product details/update/delete]....#    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # ----- Optional: Product List/Detail APIs ----- #
class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



# ----- Cart ViewSet ----- List user's cart/add to cart/update cart item/place order from cart...#

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return cart items for the logged-in user
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ----- ORDER ViewSet ---List user orders/create an order/update order/delete order.....#    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



# ----- Review ViewSet ---List all reviews/add a review/update review/delete review.....#   

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer



#............OFFER VIEWSE....[list all offers/update/delete/]
class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
