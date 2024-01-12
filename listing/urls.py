from django.urls import path
from . import views

app_name='listing'

urlpatterns = [
    path('details/<uuid:pk>',views.details,name='details'),
    path('sell/',views.sell,name='sell'),
    path('edit/<uuid:pk>/',views.edit,name='edit'),
    path('delete/<uuid:pk>/',views.archive_listing,name='delete-listing'),
    path('search/',views.search_listing,name='search'),
    path('wishlist/toggle/<uuid:vehicle_id>/', views.toggle_wishlist, name='toggle_wishlist'),

]
