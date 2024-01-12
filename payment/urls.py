from django.urls import path
from payment import views

app_name='payment'

urlpatterns = [
	path('buy-credits/', views.buy_credits, name='buy-credits'),
	path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]
