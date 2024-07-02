from django.shortcuts import render,redirect # type: ignore
from django.http import HttpResponse # type: ignore
from django.contrib.auth.models import User #type: ignore
from django.contrib.auth import authenticate,login,logout #type: ignore
from .models import Product,Cart,Order
from django.db.models import Q  # type: ignore
import razorpay #type: ignore
# Create your views here.
#for home
def home (request):
    context={}
    p=Product.objects.filter(is_active="True")
    print(p)
    context['products']=p
    return render(request,"index.html",context)

#for place_order
def order(request):
    return render(request,"place_order.html")

#for viewcart
def viewcart(request):
    cart=Cart.objects.filter(userid=request.user.id)
    context={}
    sum=0
    for x in cart:
        sum=sum+x.qty*x.pid.price
        context["total"]=sum
        context["carts"]=cart
    return render(request,"viewcart.html",context)

#for contact
def contact(request):
    return render(request,"contact.html")

#for about
def about(request):
    return render(request,"about.html")

#for login
def ulogin(request):
    context={}
    if request.method =="POST":
        user=request.POST["uname"]
        p=request.POST["upassword"]
        if user == "" or p =="":
            context["errormsg"]="Fields can not be empty."
            return render(request,"login.html",context)
        else:
            u=authenticate(username=user,password=p)
            
            print(u)
            if u is not None:
                login(request,u)
                return redirect("/home")
            else:
                context["errormsg"]="Username and password not matched."
                return render(request,"login.html",context)
    else:
        return render(request,"login.html")

    
        

#for register
def register(request):
    context={}
    if request.method == "POST":                                                                                                   
        user=request.POST["uname"]
        p=request.POST["upassword"]
        cp=request.POST["cpassword"]
        if user == "" or p == "" or cp == "":
            context["errormsg"]="Fields can not be empty"
            return render(request,"register.html",context)
        elif p != cp:
            context["errormsg"]="Password and confirm password not matched"
            return render(request,"register.html",context)
        else:
            try:
                u=User.objects.create(username=user,email=user)
                u.set_password(p)
                u.save()
                context["success"]="Registration Successfull...!"
                return render(request,"register.html",context)
            except:
                context["errormsg"]="User already exit"
                return render(request,"register.html",context)
    else:
       return render(request,"register.html")
    
    # for logout 
def ulogout(request):
    logout(request)
    return redirect('/home')

#new register
# def register(request):
#     if request.method=="GET":
#         return render(request,"register.html")
#     else:
#         user=request.POST['uname']
#         p=request.POST['upassword']
#         cp=request.POST['cpassword']
#         return HttpResponse(user+p+cp)

#for category filter
def catfilter(request,cv):
    p=Product.objects.filter(category=cv)
    context={}
    context["products"]=p
    return render(request,"index.html",context)

#for sort by price
def sortbyprice(request,pv):
    if pv=="0":
        p=Product.objects.order_by("-price").filter(is_active=True)
    
    else:
        p=Product.objects.order_by("price").filter(is_active=True)
    context={}
    context["products"]=p
    return render(request,"index.html",context)
# for filter by price
def filterbyprice(request):
    mn=request.GET["min"]
    mx=request.GET["max"]
    q1=Q(price__gte=mn)
    q2=Q(price__lte=mx)
    p=Product.objects.filter(q1&q2)
    context={}
    context["products"]=p
    return render(request,"index.html",context)

#for  product details
def productdetails(request,rid):
    context={}
    p=Product.objects.filter(id=rid)
    context["data"]=p
    return render(request,"product_details.html",context)

#for add to cart
def addcart(request,pid):
    context={}
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)
        print(u)
        print(p)
        q1=Q(pid=p[0])
        q2=Q(userid=u[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        context["data"]=p
        if n==1:
            context["msg"]="Product already exist in cart"
            return render(request,"product_details.html",context)
        else:
            cobj=Cart.objects.create(pid=p[0],userid=u[0])
            cobj.save()
            context["msg"]="Product added succssfully"
            return render(request,"product_details.html",context)
    else:
        return redirect("/login")
    
    #for update qantity
def updatequantity(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    print(q)
    if x=="1":
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    return redirect("/viewcart")

#for placeorder
import random
def placeorder(request):
    c=Cart.objects.filter(userid=request.user.id)
    orderid=random.randrange(1000,9999)
    for x in c:
        amount=x.qty* x.pid.price
        o=Order.objects.create(order_id=orderid,amt=amount,p_id=x.pid,user_id=x.userid)
        o.save()
       # x.delete()
    return redirect("/fetchorder")

#fetch order
def fetchorder(request):
    orders=Order.objects.filter(user_id=request.user.id)
    context={}
    context['orders']=orders
    sum=0
    for x in orders:
        sum=sum+x.amt
    context["totalamount"]=sum
    context['n']=len(orders)
    return render(request,"place_order.html",context)

#for payment
def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_m2nCp4tbCK0VF2", "WO7HS3vjX4exU1421Q6pUAZ2"))
    order=Order.objects.filter(user_id=request.user.id)
    context={}
    context["orders"]=order
    sum=0

    for x in order:
        sum=sum+x.amt
        orderid=x.order_id

    data = { "amount": sum*100, "currency":"INR", "receipt":orderid }
    payment = client.order.create(data=data)
    print(payment)
    context["payment"]=payment
    return render(request,"pay.html",context)

#for payment success
def paymentsuccess(request):
    return HttpResponse("Payment Done Successfully....!")




