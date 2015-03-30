import time
from .utils import uuid_str_generator
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponseRedirect
from carts.models import Cart
from .models import Order
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
    #TODO require user login
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
        return HttpResponseRedirect(reverse('cart'))
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
        print("checkout {0}".format(request.POST["stripeToken"]))
        try:
            user_stripe = request.user.userstripe.stripe_id
            customer = stripe.Customer.retrieve(user_stripe)
            print("checkout {0} stripe customer".format(customer))
        except:
            customer = None
        # Create Card Object
        if customer is not None:
            token = request.POST["stripeToken"]
            card = customer.sources.create(card=token)
            # Create a charge object; amount is sent in .01. i.e. 400 = 4.00
            charge = stripe.Charge.create(
                amount=int(new_order.final_price * 100),
                currency="usd",
                source=card,  # obtained with Stripe.js
                customer=customer,
                description="Charge for {0}".format(str(request.user.username))
            )
            print("checkout charge {0}".format(charge))
            print("checkout card {0}".format(card))
            if charge['captured']:
                print("CHARGED")

    # If order if finished delete session
    if new_order.status == "Finished":
        del request.session['cart_id']
        del request.session['items_total']
        return HttpResponseRedirect(reverse('cart'))

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
