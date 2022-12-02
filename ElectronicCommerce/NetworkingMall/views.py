from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def customer(request):
    return render(request, 'customer.html')


def goods_page(request):
    return render(request, 'goods_page.html')


def shopping_cart(request):
    return render(request, 'shopping_cart.html')


def order(request):
    return render(request, 'order.html')


def goods_management(request):
    return render(request, 'goods_management.html')


def test_page(request):
    return render(request, 'register.html')
