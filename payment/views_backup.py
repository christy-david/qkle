from django.shortcuts import render,redirect
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import Transaction,Coupon
from django.contrib import messages
from django.utils import timezone


def calculate_discount_amount(base_amount, coupon):
    # Implement your logic for calculating discount based on coupon type and value
    if coupon.discount_type == 'percentage':
        discount_amount = (coupon.discount_value / 100) * base_amount
    elif coupon.discount_type == 'flat':
        discount_amount = min(coupon.discount_value, base_amount)
    else:
        discount_amount = 0

    return discount_amount


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
)

@login_required
def buy_credits(request):
	currency = 'INR'
	base_amount = 16900
	coupon_code = request.POST.get('coupon', '')
	# request.session['coupon']=coupon_code

	if coupon_code:
		try:
				# Check if the coupon exists and is not expired
				coupon = Coupon.objects.get(coupon_code=coupon_code, expiry_date__gte=timezone.now().date())
				discount_amount = calculate_discount_amount(base_amount, coupon)
				print(discount_amount)
		except Coupon.DoesNotExist:
				messages.error(request, 'Invalid coupon code or coupon has expired.')
				return redirect('payment:buy-credits')
	else:
			discount_amount = 0

	# Calculate the total amount after applying discounts
	total_amount = base_amount - discount_amount

	# Create a Razorpay Order
	razorpay_order = razorpay_client.order.create(dict(
		amount=total_amount,
    currency=currency,
    payment_capture='0',
	))

	# order id of newly created order.
	razorpay_order_id = razorpay_order['id']
	callback_url = '/paymenthandler/'

	# we need to pass these details to frontend.
	context = {}
	context['razorpay_order_id'] = razorpay_order_id
	context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
	context['razorpay_amount'] = base_amount
	context['currency'] = currency
	context['callback_url'] = callback_url

	return render(request, 'payment/buy_credits.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': razorpay_payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is not None:
				amount = 16900
				try:

					# capture the payemt
					razorpay_client.payment.capture(razorpay_payment_id, amount)

					Transaction.objects.create(
						razorpay_payment_id=razorpay_payment_id,
						razorpay_order_id=razorpay_order_id,
						buyer_id=request.user,
						amount=amount
					)

					request.user.credits+=1
					request.user.save()

					messages.success(request,'Purchase was complete')

					# render success page on successful caputre of payment
					return render(request, 'core:index')
				except:

					# if there is an error while capturing payment.
					return render(request, 'payment/paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'payment/paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()
