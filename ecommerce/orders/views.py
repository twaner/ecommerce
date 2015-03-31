import time
from .utils import uuid_str_generator
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponseRedirect
from carts.models import Cart
from .models import Order, STATUS_CHOICES
from accounts.models import UserAddress
from accounts.forms import UserAddressForm

# Stripe API Key
try:
    stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
    stripe_secret = settings.STRIPE_SECRET_KEY
except Exception, e:
    print(str(e))
    raise NotImplementedError(str(e))

stripe.api_key = stripe_secret


# Create your views here.


def orders(request):
    template = "orders/user.html"
    context = {}
    return render(request, template, context)

@login_required()
def checkout(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse('cart'))

    # If an order exists; based on cart in session. Try and get the order; if not create an order and save()
    try:
        new_order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        new_order = Order(cart=cart)
        new_order.user = request.user
        new_order.order_id = uuid_str_generator()
        new_order.save()
    except:
        new_order = None
        return HttpResponseRedirect(reverse('cart'))
    final_amount = 0
    if new_order is not None:
        new_order.sub_total = cart.total
        final_amount = new_order.get_final_amount()
        new_order.final_price = final_amount
        new_order.save()
    try:
        address_added = request.GET.get("address_added")
    except Exception, e:
        address_added = None
    # if address exi
    if address_added is None:
        address_form = UserAddressForm()
    else:
        address_form = None
    current_addresses = UserAddress.objects.filter(user=request.user)
    billing_addresses = UserAddress.objects.get_billing_addresses(user=request.user)

    # request handler
    if request.method == "POST":
        try:
            user_stripe = request.user.userstripe.stripe_id
            customer = stripe.Customer.retrieve(user_stripe)
        except:
            customer = None
        # Create Card Object
        if customer is not None:
            shipping_address = request.POST['shipping_address']
            billing_address = request.POST['billing_address']  # .get('billing_address')
            try:
                billing_address_instance = UserAddress.objects.get(id=billing_address)
            except:
                billing_address_instance = None
            try:
                shipping_address_instance = UserAddress.objects.get(id=shipping_address)
            except:
                shipping_address_instance = None
            # Create card
            token = request.POST["stripeToken"]
            card = customer.sources.create(card=token)
            card.address_line1 = billing_address_instance.address or None
            card.address_line2 = billing_address_instance.address2 or None
            card.address_city = billing_address_instance.city or None
            card.address_zip = billing_address_instance.zipcode or None
            card.address_country = billing_address_instance.country or None
            card.address_state = billing_address_instance.state or None
            card.save()
            # Create a charge object; amount is sent in .01. i.e. 400 = 4.00
            charge = stripe.Charge.create(
                amount=int(final_amount * 100),
                currency="usd",
                source=card,  # obtained with Stripe.js
                customer=customer,
                description="Charge for {0}".format(str(request.user.username))
            )
            # If the charge status is captured - Update order status; save; delete session data;
            # add a message and reverse to orders page
            if charge['captured']:
                new_order.status = STATUS_CHOICES[2][0]
                new_order.shipping_address = shipping_address_instance
                new_order.billing_address = billing_address_instance
                new_order.save()
                del request.session['cart_id']
                del request.session['items_total']
                messages.success(request, "Thank you for your order it has been completed!")
                return HttpResponseRedirect(reverse('orders'))

    # render section
    template = "orders/checkout.html"
    context = {
        "address_form": address_form,
        "current_addresses": current_addresses,
        "billing_addresses": billing_addresses,
        "stripe_pub": stripe_pub,
        "order": new_order,
        }
    return render(request, template, context)
