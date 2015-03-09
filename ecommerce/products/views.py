from django.shortcuts import render, Http404
from .models import Product
# Create your views here.


def home(request):
    products = Product.objects.all()
    context = {'products': products}
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
        context = {'product': product}
        template = 'products/single.html'
        return render(request, template, context)
    except Product.DoesNotExist:
        raise Http404
