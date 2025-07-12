from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CategoryViewSet, ProductViewSet, CartViewSet,
    OrderViewSet, ReviewViewSet,
    ProductListAPIView, ProductDetailAPIView,OfferViewSet
)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('carts', CartViewSet, basename='cart') 
router.register('orders', OrderViewSet)
router.register('reviews', ReviewViewSet)
router.register('offers', OfferViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Optional APIView routes
    path('api/products/', ProductListAPIView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
]
