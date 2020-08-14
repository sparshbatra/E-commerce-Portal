from django.shortcuts import render
from django.http import HttpResponse
from math import ceil
from .models import Product

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)- (n//4))
    # params = {'product':products, 'no_of_slides':nSlides, 'range':range(1, nSlides)}

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds}
    return render(request,"shoppingapp/index.html", params)

def about(request):
    return render(request, 'shoppingapp/about.html')

def contact(request):
    return render(request, 'shoppingapp/contact.html')

def tracker(request):
    return render(request, 'shoppingapp/tracker.html')

def search(request):
    return render(request, 'shoppingapp/search.html')

def productView(request):
    return render(request, 'prodView.html')

def checkout(request):
    return render(request, 'checkout.html')