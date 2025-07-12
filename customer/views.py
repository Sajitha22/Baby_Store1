from django.shortcuts import render,redirect
from customer.forms import RegistrationForm,LoginForm,CheckoutForm
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.generic import TemplateView
from store.models import Category,Product,Cart,Order,Offer,Review
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.views.generic import ListView
from django.shortcuts import  reverse
from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ReviewForm






class SignUpView(View):
    def get(self,request,*args,**kwrags):
        form=RegistrationForm()
        return render(request,"signup.html",{"form":form})
    def post(self,request,*args,**kw):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signup")
        else:
            return render(request,"signup.html",{"form":form})

class SignInView(View):
    def get(self,request,*args,**kw):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
          uname=form.cleaned_data.get("username")
          pwd=form.cleaned_data.get("password")
          print(uname,pwd)
          usr=authenticate(request,username=uname,password=pwd)
          if usr:
            login(request,usr)
            return redirect("home")
          else:
             
           return render(request,"login.html",{"form":form})

        else:
            return render(request,"login.html",{"form":form})
               
        
        
class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # active categories
        context["categories"] = Category.objects.filter(is_active=True)

        # active offers → corresponding products
        active_offers = Offer.objects.filter(
            isAvailable=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
        # Grab unique products
        context["offer_products"] = [offer.product for offer in active_offers]

        return context




class CategoryProductsView(TemplateView):
    template_name = "category_products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("id")
        category = Category.objects.get(id=category_id)
        context["category"] = category
        context["products"] = Product.objects.filter(category=category, is_active=True)
        return context





def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.review_set.all().order_by('-created_at')  # Get all reviews for the product

    return render(request, 'product_details.html', {
        'product': product,
        'reviews': reviews,
    })





def get_active_offer(product):
    today = datetime.date.today()
    return Offer.objects.filter(
        product=product,
        isAvailable=True,
        start_date__lte=today,
        end_date__gte=today
    ).first()




@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = Cart.objects.get_or_create(
            product=product,
            user=request.user,
            status="in-cart"
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect("home")  # or redirect to category/products page
    








class CartListView(LoginRequiredMixin, TemplateView):
    template_name = "cart_list.html"
    login_url = '/login/'  # or set in settings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = Cart.objects.filter(user=self.request.user, status="in-cart")

        for item in cart_items:
            offer = Offer.objects.filter(
                product=item.product,
                isAvailable=True,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            ).first()

            if offer:
                item.discounted_price = round(item.product.price * (1 - offer.discount / 100), 2)
            else:
                item.discounted_price = item.product.price

            item.total_price = item.discounted_price * item.quantity

        total = sum(item.total_price for item in cart_items)

        context["cart_items"] = cart_items
        context["total"] = total
        return context



class RemoveCartItemView(LoginRequiredMixin, View):
    def post(self, request, id):
        cart_item = get_object_or_404(Cart, id=id, user=request.user, status="in-cart")
        cart_item.delete()
        messages.success(request, "🗑️ Item removed from cart successfully.")
        return redirect("cart_list")  # Make sure this matches your cart page name
    

class UpdateCartQuantityView(LoginRequiredMixin, View):
    def post(self, request, id):
        cart_item = get_object_or_404(Cart, id=id, user=request.user, status="in-cart")
        new_qty = request.POST.get("quantity")
        if new_qty and int(new_qty) > 0:
            cart_item.quantity = int(new_qty)
            cart_item.save()
            messages.success(request, "Quantity updated successfully.")
        else:
            messages.error(request, "Please enter a valid quantity.")
        return redirect("cart_list")    
    



    



@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        form = CheckoutForm()
        cart_items = Cart.objects.filter(user=request.user, status="in-cart")
        total = sum(item.quantity * item.product.price for item in cart_items)
        return render(request, "checkout.html", {
            "form": form,
            "cart_items": cart_items,
            "total": total
        })

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST)
        cart_items = Cart.objects.filter(user=request.user, status="in-cart")
        if form.is_valid():
            address = form.cleaned_data["address"]
            for item in cart_items:
                Order.objects.create(
                    product=item.product,
                    user=request.user,
                    address=address,
                    status="order-placed",
                    expected_deliverydate=datetime.date.today() + datetime.timedelta(days=5)
                )
                item.status = "order-placed"
                item.save()

            return redirect("thank_you")  # ✅ Optional: redirect to 'thank_you' page

        total = sum(item.quantity * item.product.price for item in cart_items)
        return render(request, "checkout.html", {
            "form": form,
            "cart_items": cart_items,
            "total": total
        })
    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = Cart.objects.filter(user=self.request.user, status="in-cart")

        for item in cart_items:
            offer = Offer.objects.filter(
                product=item.product,
                isAvailable=True,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            ).first()
            item.offer = offer
            if offer:
                item.discounted_price = round(item.product.price * (1 - offer.discount / 100), 2)
            else:
                item.discounted_price = item.product.price

            item.total_price = item.discounted_price * item.quantity

        context["cart_items"] = cart_items
        context["total"] = sum(item.total_price for item in cart_items)
        return context



def thank_you_view(request):
    return render(request, "thank_you.html")





class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "order_history.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).exclude(
            status="cancelled"
        ).order_by("-created_date")

class CancelOrderView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, id=pk, user=request.user)
        
        if order.status in ["order-placed", "in-transit"]:
            order.status = "cancelled"
            order.save()
            messages.success(request, "Your order has been cancelled.")
        else:
            messages.warning(request, "Order cannot be cancelled at this stage.")
        
        return redirect("order_history")
    




@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            from django.shortcuts import redirect, reverse

        return redirect(reverse('product_detail', kwargs={'pk': product.id}))


    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'product': product})



@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    product_id = review.product.id
    review.delete()
    return redirect('product_detail', pk=product_id)
