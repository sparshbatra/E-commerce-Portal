from django.shortcuts import render
from django.http import HttpResponse
from math import ceil
from .models import Product, Contact, Orders, OrderUpdate
import json

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
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shoppingapp/contact.html', {'thank': thank})

# def tracker(request):
#     if request.method=="POST":
#         orderId = request.POST.get('orderId', '')
#         email = request.POST.get('email', '')
#         # console.log(OrderUpdate.objects.all())
#         # return HttpResponse(f"{orderId} and {email}")

#         try:
#             # console.log("Tried")
#             order = Orders.objects.filter(order_id=orderId, email=email)
#             console.log(order)
#             if len(order)>0:
#                 update = OrderUpdate.objects.filter(order_id=orderId)
#                 updates = []
#                 for item in update:
#                     updates.append({'text': item.update_desc, 'time': item.timestamp})
#                     response = json.dumps(updates, default=str)
#                 console.log(response)
#                 return HttpResponse(response)
#             else:
#                 return HttpResponse(f"{not found}")

#                 pass
#         except Exception as e: 
#             return HttpResponse(f"{Exception}")

#     return render(request, 'shoppingapp/tracker.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shoppingapp/tracker.html')


def search(request):
    return render(request, 'shoppingapp/search.html')

def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    return render(request, 'shoppingapp/prodView.html', {'product':product[0]})
    #product[0] because it is a single item list

def checkout(request):
    # thank = False
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed.")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shoppingapp/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shoppingapp/checkout.html')