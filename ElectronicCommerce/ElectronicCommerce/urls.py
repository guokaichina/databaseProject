"""ElectronicCommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from NetworkingMall import views


urlpatterns = [
    path('search/<str:keyword>/', views.search_goods, name='search_goods'),
    path('search/', views.search_goods, name='search_nothing'),
    path('admin/', admin.site.urls),
    path('', views.test_page),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('good/<int:goods_id>', views.goods_page, name='goods'),
    path('order/<int:customer_id>', views.order, name='order'),
    path('shopping_cart/<int:customer_id>', views.shopping_cart, name='shopping_cart'),
    path('seller_index/<int:seller_id>', views.seller_index, name='seller_index'),
    path('goods_add/', views.goods_add, name='goods_add'),
    path('logout/', views.logout, name='logout'),
]
