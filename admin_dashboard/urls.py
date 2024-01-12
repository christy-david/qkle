from django.urls import path
from . import views

app_name='admin_dashboard'

urlpatterns = [
    path('',views.admin_home,name='admin-home'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('edit-vehicle/<uuid:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('delete-image/<uuid:image_id>/', views.delete_image, name='delete_image'),
    path('categories/', views.list_categories, name='list_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<uuid:category_id>/', views.edit_category, name='edit_category'),
    path('categories/archive/<uuid:category_id>/', views.archive_category, name='archive_category'),
    path('categories/unarchive/<uuid:category_id>/', views.unarchive_category, name='unarchive_category'),
    path('sales-report/', views.SalesReportView.as_view(), name='sales_report'),
    path('download-transactions-csv/', views.DownloadTransactionsCSV.as_view(), name='download_transactions_csv'),
     path('list_ads/', views.list_ads, name='list_ads'),
    path('add_ad/', views.add_ad, name='add_ad'),
    path('edit_ad_image/<uuid:campaign_id>/', views.edit_ad_image, name='edit_ad_image'),
    path('delete_ad/<uuid:campaign_id>/', views.delete_ad, name='delete_ad'),
]
