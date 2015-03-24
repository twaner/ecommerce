from django.shortcuts import render, Http404
from marketing.forms import EmailForm
from marketing.models import MarketingMessage, Slider
from .models import Product, ProductImage
# Create your views here.


def home(request):
    """
    Home View. Homepage for website.
    :param request: Http request.
    :return: Homepage.
    """
    sliders = Slider.objects.all_featured()
    products = Product.objects.all()
    context = {
        'products': products,
        "sliders": sliders,
    }

    template = "products/home.html"
    return render(request, template, context)


def allview(request):
    """
    All View. This page shows all products. Will delete the session marketing_message.
    :param request: Http request.
    :return: Products page.
    """
    del request.session['marketing_message']
    products = Product.objects.all()
    context = {'products': products}
    template = 'products/all.html'
    return render(request, template, context)


def single(request, slug):
    """
    Single View. This page shows a single product.
    :param request: Http request.
    :param slug: Slug for product.
    :return: Single product page. :raise Http404:
    """
    try:
        print(slug)
        product = Product.objects.get(slug=slug)
        images = product.productimage_set.all()
        # images = product.objects.filter(product=product)
        context = {'product': product, "images": images}
        template = 'products/single.html'
        return render(request, template, context)
    except Product.DoesNotExist:
        raise Http404


def search(request):
    """
    Search View. This page shows the results of the user's search.
    :param request:Http request.
    :return: Page of filtered products or the home page.
    """
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        products = Product.objects.filter(title__icontains=q)
        context = {'query': q, 'products': products}
        template = "products/results.html"
    else:
        context = {}
        template = "products/home.html"
    return render(request, template, context)