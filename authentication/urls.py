from django.urls import path
from . import views

app_name='authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path("logout/", views.logout_user, name="logout"),
    path('sign-up/',views.sign_up,name="sign-up"),
    path('otp_verification/',views.otp_verification,name="otp_verification")
]
