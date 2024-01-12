from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path('',include('core.urls')),
    path('listing/',include('listing.urls')),
    path('',include('authentication.urls')),
    path('profile/',include('user_profile.urls')),
    path('inbox/',include('chat.urls')),
    path('dashboard/',include('admin_dashboard.urls')),
    path('',include('payment.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
