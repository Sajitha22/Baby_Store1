from django.contrib import admin

from django.contrib import admin
# Register your models here.
from store.models import Category,Product,Cart,Order,Offer,Review
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Offer)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__product_name', 'user__username', 'comment')
    list_filter = ('rating', 'created_at')

admin.site.register(Review, ReviewAdmin)





