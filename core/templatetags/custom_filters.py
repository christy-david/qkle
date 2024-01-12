# yourapp/templatetags/custom_filters.py
from django import template
from user_profile.models import Wishlist

register = template.Library()

@register.filter(name='get')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='is_in_wishlist')
def is_in_wishlist(vehicle, user):
    return Wishlist.is_vehicle_in_wishlist(user, vehicle)

