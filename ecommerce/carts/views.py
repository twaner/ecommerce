from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Cart, CartItem

# Create your views here.
from products.models import Product, Variation


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
                print v
            except:
                pass

        # # each cart item is being created and will be associated with its cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            print("!!! Update cart Created !!!")

        # Delete cart item
        if int(qty) <= 0:
            cart_item.delete()
        else:
            if len(product_var) > 0:
                cart_item.variations.clear()
                try:
                    for i in product_var:
                        cart_item.variations.add(i)
                except:
                    pass
            cart_item.quantity = qty
            cart_item.save()

        new_total = 0.0
        # cart item is a fk related set of objects
        for i in cart.cartitem_set.all():
            line_total = float(i.product.price) * i.quantity
            new_total += line_total
            cart_item.line_total = line_total
            cart_item.save()
        request.session['items_total'] = cart.cartitem_set.count()

        cart.total = new_total
        cart.save()
        return HttpResponseRedirect(reverse("cart"))
    else:
        return HttpResponseRedirect(reverse("cart"))
