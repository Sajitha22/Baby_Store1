from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.utils import timezone

# -------- Choices -------- #
GENDER_CHOICES = [
    ('boy', 'Boy'),
    ('girl', 'Girl'),
    ('unisex', 'Unisex'),
]

AGE_GROUP_CHOICES = [
    ('0-3m', '0-3 months'),
    ('3-6m', '3-6 months'),
    ('6-12m', '6-12 months'),
    ('1-2y', '1-2 years'),
    ('2-3y', '2-3 years'),
    ('3-5y', '3-5 years'),
]

# -------- Models -------- #
class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    STATUS_CHOICES = [
        ("in-cart", "In Cart"),
        ("order-placed", "Order Placed"),
        ("cancelled", "Cancelled"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="in-cart")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity})"



class Order(models.Model):
    STATUS_CHOICES = [
        ("order-placed", "Order Placed"),
        ("shipped", "Shipped"),
        ("in-transit", "In Transit"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
        ("return", "Returned"),
    ]

    def get_delivery_date():
        return datetime.date.today() + datetime.timedelta(days=5)

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="order-placed")
    expected_deliverydate = models.DateField(default=get_delivery_date)
    address = models.CharField(max_length=260, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.product_name} - {self.status}"





class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    comment = models.CharField(max_length=240)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} review by {self.user.username}"






class Offer(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='offers')
    discount = models.PositiveIntegerField(default=0)
    isAvailable = models.BooleanField(default=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def is_active(self):
        today = timezone.now().date()
        return self.isAvailable and (not self.start_date or self.start_date <= today) and (not self.end_date or self.end_date >= today)

    def discounted_price(self):
        return round(self.product.price - (self.product.price * self.discount / 100), 2)

    def __str__(self):
        return f"{self.discount}% off on {self.product.product_name}"

