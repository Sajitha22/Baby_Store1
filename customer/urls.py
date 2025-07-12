from django.urls import path
from customer import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.SignInView.as_view(), name="signin"),
    path("home/", views.IndexView.as_view(), name="home"),
    path("category/<int:id>/", views.CategoryProductsView.as_view(), name="category_products"),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path("add-to-cart/<int:product_id>/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("cart/", views.CartListView.as_view(), name="cart_list"),
    path("cart/remove/<int:id>/", views.RemoveCartItemView.as_view(), name="remove_cart_item"),
    path("cart/update/<int:id>/", views.UpdateCartQuantityView.as_view(), name="update_cart_item"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("orders/", views.OrderHistoryView.as_view(), name="order_history"),
    path("orders/<int:pk>/cancel/", views.CancelOrderView.as_view(), name="cancel_order"),
    path("thank-you/", views.thank_you_view, name="thank_you"),
    path('logout/', LogoutView.as_view(next_page='signin'), name='logout'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),



]
