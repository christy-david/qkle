from django.urls import path
from . import views

app_name='chat'

urlpatterns = [
    path('new/<uuid:vehicle_pk>/',views.new_chat,name='new-chat'),
    path('inbox/',views.inbox,name='inbox'),
    path('<int:pk>/', views.detail, name='detail'),
]
