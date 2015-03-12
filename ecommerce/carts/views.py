from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Cart, CartItem

# Create your views here.
from products.models import Product


def view(request):
    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
    if the_id:
        cart = Cart.objects.get(id=the_id)
        context = {"cart": cart}
    else:
        empty_message = "Your cart is empty, please keep shopping."
        context = {"empty": True, "empty_message": empty_message}
    template = 'cart/view.html'
    return render(request, template, context)


def update_cart(request, slug):
    request.session.set_expiry(120000)
    # Get qty, attr
    try:
        qty = request.GET.get('qty')
        update_qty = True
    except:
        qty = None
        update_qty = False

    try:
        attr = request.GET.get('attr')
    except:
        attr = None

    # Get Cart Id
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id
    cart = Cart.objects.get(id=the_id)
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        pass
    except:
        pass
    # each cart item is being created and will be associated with its cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        print("!!! Update cart Created !!!")

    # if not cart_item in cart.items.all():
    #     cart.items.add(cart_item)
    # else:
    #     cart.items.remove(cart_item)

    # Delete cart item
    if update_qty and qty:
        if int(qty) == 0:
            cart_item.delete()
        else:
            cart_item.quantity = qty
            cart_item.save()
    else:
        pass
    new_total = 0.0
    # cart item is a fk related set of objects
    for i in cart.cartitem_set.all():
        line_total = float(i.product.price) * i.quantity
        new_total += line_total
    request.session['items_total'] = cart.cartitem_set.count()

    cart.total = new_total
    cart.save()
    return HttpResponseRedirect(reverse("cart"))
