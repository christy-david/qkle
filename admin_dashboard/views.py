from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from authentication.models import CustomUser
from listing.models import Vehicle,Image,Category
from django.contrib import messages
from .forms import VehicleEditForm,CategoryForm
from django.http import JsonResponse
from listing.forms import ImageForm
from django.shortcuts import render
from django.views.generic import TemplateView
from payment.models import Transaction
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.db.models.functions import TruncDay
from django.db.models import Sum
import plotly.express as px
import plotly.io as pio
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
import csv
from django.urls import reverse
from ads.models import Ad
from admin_dashboard.forms import AdForm

@login_required
@never_cache
def admin_home(request):
    if request.user.is_superuser:
        user_id = request.POST.get('user_id')
        if user_id is not None:
            user = get_object_or_404(CustomUser, id=user_id)

            # Toggle the is_banned status
            user.is_banned = not user.is_banned
            user.save()

            # Archive or unarchive vehicles based on the is_banned status
            vehicles = Vehicle.objects.filter(sold_by=user)
            if user.is_banned:
                # Archive vehicles
                vehicles_to_archive = vehicles.filter(archived=False)
                vehicles_to_archive.update(archived=True)

                # Provide feedback to the user
                messages.success(request, f'User {user.username} has been banned, and their vehicles have been archived.')
            else:
                # Unarchive vehicles
                vehicles_to_unarchive = vehicles.filter(archived=True)
                vehicles_to_unarchive.update(archived=False)

                # Provide feedback to the user
                messages.success(request, f'User {user.username} has been unbanned, and their vehicles have been unarchived.')

        users = CustomUser.objects.all()
        context = {'users': users}
        return render(request, 'admin_dashboard/dashboard.html', context)
    else:
        return render(request, 'core/unauthorized.html')
    

@never_cache
def vehicles(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            vehicle_id = request.POST.get('vehicle_id')
            action = request.POST.get('action')
            print(action)

            if vehicle_id and action in ['publish', 'unpublish']:
                vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)

                if action == 'publish':
                    vehicle.published = True
                    vehicle.save()
                    messages.success(request, f'Vehicle {vehicle.vehicle_id} has been published.')
                elif action == 'unpublish':
                    vehicle.published = False
                    vehicle.save()
                    messages.success(request, f'Vehicle {vehicle.vehicle_id} has been unpublished.')

                return redirect('admin_dashboard:vehicles')
            
        # Corrected indentation here
        vehicles = Vehicle.objects.filter(is_sold=False,archived=False).prefetch_related('images')

        context = {
            'vehicles': vehicles,
        }

        return render(request, 'admin_dashboard/listings.html', context)
    else:
        return render(request, 'core/unauthorized.html')
    
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, vehicle_id=vehicle_id)

    if request.method == 'POST':
        form = VehicleEditForm(request.POST, instance=vehicle)
        image_form = ImageForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            form.save()

            new_images = request.FILES.getlist('new_images')
            for image in new_images:
                Image.objects.create(vehicle_id=vehicle, image=image)

            return redirect('admin_dashboard:vehicles')
    else:
        form = VehicleEditForm(instance=vehicle)
        image_form = ImageForm()

    images = vehicle.images.all()

    context = {
        'form': form,
        'image_form': image_form,
        'vehicle': vehicle,
        'images': images,
    }
    return render(request, 'admin_dashboard/edit_vehicle.html', context)

def delete_image(request, image_id):
    image = get_object_or_404(Image, image_id=image_id)
    vehicle_id = image.vehicle_id.vehicle_id
    image.delete()
    return JsonResponse({'success': True, 'vehicle_id': str(vehicle_id)})

def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'admin_dashboard/list_categories.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard:list_categories')
    else:
        form = CategoryForm()

    return render(request, 'admin_dashboard/add_category.html', {'form': form})

def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard:list_categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'admin_dashboard/edit_category.html', {'form': form})

def archive_category(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    category.archived = True
    category.save()

    # Archive vehicles associated with the category
    vehicles_to_archive = category.items.filter(archived=False)
    vehicles_to_archive.update(archived=True)

    messages.success(request, f'Category "{category.name}" has been archived.')
    return redirect('admin_dashboard:list_categories')

def unarchive_category(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    category.archived = False
    category.save()

    # Unarchive vehicles associated with the category
    vehicles_to_unarchive = category.items.filter(archived=True)
    vehicles_to_unarchive.update(archived=False)

    messages.success(request, f'Category "{category.name}" has been unarchived.')
    return redirect('admin_dashboard:list_categories')



class SalesReportView(TemplateView):
    template_name = 'admin_dashboard/sales_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch data from the database
        transactions = Transaction.objects.all()

        # Calculate daily sales
        daily_sales = self.calculate_daily_sales(transactions)

        # Add transactions to context
        context['transactions'] = transactions

        # Generate and save the plot
        plot_url = self.generate_plot(daily_sales)

        # Add data to context
        context['plot_url'] = plot_url

        return context

    def calculate_daily_sales(self, transactions):
        daily_sales = {}
        for transaction in transactions:
            date = transaction.timestamp.date()
            if date in daily_sales:
                daily_sales[date] += transaction.amount
            else:
                daily_sales[date] = transaction.amount
        return daily_sales

    def generate_plot(self, data):
        # Create a plot
        plt.figure(figsize=(10, 6))
        plt.plot(data.keys(), data.values(), marker='o', linestyle='-', color='b')
        plt.title('Daily Sales Report')
        plt.xlabel('Date')
        plt.ylabel('Sales Amount (USD)')
        plt.grid(True)

        # Save plot to BytesIO
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)
        plt.close()

        # Encode the image to base64
        plot_url = base64.b64encode(image_stream.read()).decode('utf-8')
        return f'data:image/png;base64,{plot_url}'


def list_ads(request):
    ads = Ad.objects.all()
    return render(request, 'admin_dashboard/list_ads.html', {'ads': ads})

def add_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard:list_ads')
    else:
        form = AdForm()
    return render(request, 'admin_dashboard/add_ad.html', {'form': form})

def edit_ad_image(request, campaign_id):
    ad = get_object_or_404(Ad, campaign_id=campaign_id)

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard:list_ads')
    else:
        form = AdForm(instance=ad)

    return render(request, 'admin_dashboard/edit_ad_image.html', {'form': form, 'ad': ad})

def delete_ad(request, campaign_id):
    ad = get_object_or_404(Ad, campaign_id=campaign_id)

    if request.method == 'POST':
        ad.delete()
        return redirect('admin_dashboard:list_ads')

    return render(request, 'admin_dashboard/delete_ad.html', {'ad': ad})


class DownloadTransactionsCSV(View):
    def get(self, request, *args, **kwargs):
        # Fetch data from the database
        transactions = Transaction.objects.all()

        # Create CSV content
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

        # Create a CSV writer and write header
        writer = csv.writer(response)
        writer.writerow(['Payment ID', 'Razorpay Payment ID', 'Razorpay Order ID', 'Buyer ID', 'Amount', 'Credits', 'Coupon', 'Timestamp'])

        # Write transaction data
        for transaction in transactions:
            writer.writerow([
                transaction.payment_id,
                transaction.razorpay_payment_id,
                transaction.razorpay_order_id,
                transaction.buyer_id,
                transaction.amount,
                transaction.credits,
                transaction.coupon.coupon_code if transaction.coupon else '',
                transaction.timestamp,
            ])

        return HttpResponseRedirect(reverse('admin_dashboard:admin-home'))