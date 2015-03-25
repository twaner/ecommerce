import time
from .utils import uuid_str_generator
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from carts.models import Cart
from .models import Order
from accounts.models import UserAddress
from accounts.forms import UserAddressForm

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
        print "checkout - first except no session cart_id"
        return HttpResponseRedirect(reverse('cart'))

    # If an order exists; based on cart in session. Try and get the order; if not create an order and save()
    try:
        new_order = order.objects.get(cart=cart)
    except Order.DoesNotExist:
        new_order = Order(cart=cart)
        new_order.user = request.user
        new_order.order_id = uuid_str_generator()
        new_order.save()
    except:
        # Handle Error msg
        print "checkout - except other than order DoesNotExist"
        return HttpResponseRedirect(reverse('cart'))
    address_form = UserAddressForm(request.POST or None)
    if address_form.is_valid():
        new_address = address_form.save(commit=False)
        new_address.user = request.user
        new_address.save()
    # If order if finished delete session
    if new_order.status == "Finished":
        del request.session['cart_id']
        del request.session['items_total']
        print "checkout - del the session"
        return HttpResponseRedirect(reverse('cart'))

    template = "orders/checkout.html"
    context = {"address_form": address_form}
    return render(request, template, context)




