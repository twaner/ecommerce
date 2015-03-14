import time
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from carts.models import Cart
from .models import Order
from .utils import uuid_str_generator
# Create your views here.


def orders(request):
    template = "orders/user.html"
    context = {}
    return render(request, template, context)


def checkout(request):
    #TODO require user login
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse('cart'))
    new_order, created = Order.objects.get_or_create(cart=cart)
    if created:
        # TODO assign user to order
        # TODO assign address
        r = uuid_str_generator()
        print("ORDER ID %s" % r)
        new_order.order_id = r
        new_order.save()
    new_order.user = request.user
    new_order.save()
    # If order if finished delete session
    if new_order.status == "Finished":
        del request.session['cart_id']
        del request.session['items_total']
        return HttpResponseRedirect(reverse('cart'))

    template = "products/home.html"
    context = {}
    return render(request, template, context)