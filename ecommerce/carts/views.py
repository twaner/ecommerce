from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Cart, CartItem
from .helper_methods import get_cart_helper
# Create your views here.
from products.models import Product, Variation


def view(request):
    # try:
    #     the_id = request.session['cart_id']
    # except:
    #     the_id = None
    # if the_id:
    #     cart = Cart.objects.get(id=the_id)
    """
    Cart View. This page shows items that are in the user's cart.
    :param request: Http request.
    :return:Cart page.
    """
    cart, context = get_cart_helper(request, "cart_id")
    if cart is not None:
        new_total = 0.0
        # cart item is a fk related set of objects
        for i in cart.cartitem_set.all():
            line_total = float(i.product.price) * i.quantity
            new_total += line_total
            i.line_total = line_total
            i.save()
        request.session['items_total'] = cart.cartitem_set.count()

        cart.total = new_total
        cart.save()
        context = {"cart": cart}
    else:
        empty_message = "Your cart is empty, please keep shopping."
        context = {"empty": True, "empty_message": empty_message}
    template = 'cart/view.html'
    return render(request, template, context)


def remove_from_cart(request, id):
    """
    Remove View. This page removes an item from a user's cart.
    :param request: Http request.
    :param id: Product Id.
    :return: Cart page.
    """
    cart, context = get_cart_helper(request, "cart_id")
    if cart is None:
        return HttpResponseRedirect(reverse("cart"))
    cart_item = CartItem.objects.get(id=id)
    cart_item.cart = None
    cart_item.save()
    # send success message
    return HttpResponseRedirect(reverse("cart"))


def add_to_cart(request, slug):
    """
    Add To Cart View. Adds an item to the cart. This sets the session's expiration. Gets the user's existing cart or
    creates a new cart. Then adds the product to the cart if the product exists.
    :param request: Http request.
    :param slug: Product's slug.
    :return: Cart page.
    """
    request.session.set_expiry(120000)
    # Get the cart
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

    # Handle POST
    product_var = []
    if request.method == "POST":
        qty = request.POST['qty']
        for item in request.POST:
            key = item
            val = request.POST[key]
            try:
                v = Variation.objects.get(product=product, category__iexact=key, title__iexact=val)
                #v = Variation.objects.get(id=val)
                product_var.append(v)
            except:
                pass

        # # each cart item is being created and will be associated with its cart
        cart_item = CartItem.objects.create(cart=cart, product=product)

        if len(product_var) > 0:
            cart_item.variations.add(*product_var)
        cart_item.quantity = qty
        cart_item.save()
        # TODO success msg
        return HttpResponseRedirect(reverse("cart"))
    else:
        # TODO error msg
        return HttpResponseRedirect(reverse("cart"))
