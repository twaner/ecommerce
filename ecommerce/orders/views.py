import time
from .utils import uuid_str_generator
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from carts.models import Cart
from .models import Order
from accounts.models import UserAddress
from accounts.forms import UserAddressForm

# Stripe API Key
try:
    stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
except Exception, e:
    print(str(e))
    raise NotImplementedError(str(e))


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
        }
    return render(request, template, context)
