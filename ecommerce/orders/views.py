import time
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from carts.models import Cart
from .models import Order

# Create your views here.


def checkout(request):
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
        new_order.order_id = str(time.time())
        new_order.save()

    # If order if finished delete session
    if new_order.status == "Finished":
        del request.session['cart_id']
        del request.session['items_total']
        return HttpResponseRedirect(reverse('cart'))

    template = "products/home.html"
    context = {}
    return render(request, template, context)