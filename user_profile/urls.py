from django.urls import path
from user_profile import views

app_name='user_profile'

urlpatterns = [
    path('listings/',views.user_listings,name='user-listings'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('reset-password/',views.reset_password,name='reset_password'),
    path('otp_verification/',views.otp_verification,name="otp_verification"),
    path('edit/', views.edit_profile, name='edit-profile'),
    path('view/<uuid:user_id>/', views.view_profile, name='view-profile'),
    path('reset_password/', views.reset_password_view, name='reset-password'),
]
