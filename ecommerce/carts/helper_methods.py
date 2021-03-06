__author__ = 'taiowawaner'
from .models import Cart


def request_get_helper(request, name):
    """
    Returns a tuple of values from a request.
    :param request: request.
    :param name: name of value to get from request.
    :return:
    """
    try:
        val = request.GET.get(name)
        updated = True
    except:
        val = None
        updated = False
    return val, updated


def get_cart_helper(request, cart_id):
    cart = None
    the_id = None
    context = {}
    try:
        the_id = request.session[cart_id]
        cart = Cart.objects.get(id=the_id)
        context = {"cart": cart}
    except:
        the_id = None
    return cart , context