from django import template
from store.models import Offer
from django.utils import timezone

register = template.Library()

@register.simple_tag
def get_offer(product):
    return Offer.objects.filter(
        product=product,
        isAvailable=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).first()

@register.simple_tag
def get_discounted_price(product):
    offer = Offer.objects.filter(
        product=product,
        isAvailable=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).first()
    if offer:
        return round(product.price - (product.price * offer.discount / 100), 2)
    return product.price

