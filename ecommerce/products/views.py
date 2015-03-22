from django.shortcuts import render, Http404
from marketing.models import MarketingMessage
from .models import Product, ProductImage
# Create your views here.


def home(request):
    products = Product.objects.all()
    marketing_message = MarketingMessage.objects.all()[0]
    print("HOME {0}".format(marketing_message))
    context = {'products': products, "marketing_message": marketing_message}
    template = "products/home.html"
    return render(request, template, context)


def allview(request):
    products = Product.objects.all()
    context = {'products': products}
    template = 'products/all.html'
    return render(request, template, context)


def single(request, slug):
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