"""
URL configuration for amazonproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from ecomapp import views
from django.conf.urls.static import static # type: ignore
from django.conf import settings # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/",views.home),
    #path("pdetails/",views.product),
    path("viewcart/",views.viewcart),
    path("contact/",views.contact),
    path("about/",views.about),
    path("login/",views.ulogin),
    path("register/",views.register),
    path("logout/",views.ulogout),
    #for the category filter
    path("catfilter/<cv>/",views.catfilter),
    #for the sort by price
    path("sortbyprice/<pv>/",views.sortbyprice),
    #for the filter by price
    path("filterbyprice/",views.filterbyprice),
    #for productdetails
    path("pdetails/<rid>/",views.productdetails),
    #for addtocart
    path("addcart/<pid>/",views.addcart),
    #for updateqty
    path("updateqty/<x>/<cid>/",views.updatequantity),
    #for placeorder
    path("porder/",views.placeorder),
    #for fetchorder
    path("fetchorder/",views.fetchorder),
    #for payment
    path("makepayment/",views.makepayment),
    #for paymentsuccess
    path("paysuccess/",views.paymentsuccess),
   
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)