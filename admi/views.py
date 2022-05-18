
from django.shortcuts import render,redirect
from store.models import Product
# Create your views here.
from django import forms

from .models import AdmiLogin, Userdata

class AdmiLoginForm(forms.Form):
    name = forms.CharField(label = 'name', max_length=254)
    password = forms.CharField(label = 'password', max_length=16,widget = forms.PasswordInput)
class UserdataForm(forms.Form):
    name = forms.CharField(label = 'name', max_length=254)
    password = forms.CharField(label = 'password', max_length=16,widget = forms.PasswordInput)#,widget = forms.PasswordInput
    age = forms.IntegerField(label='age',min_value=1,max_value=150)
class Sign(forms.Form):
    name = forms.CharField(label = 'name', max_length=254)
    password = forms.CharField(label = 'password', max_length=16,widget = forms.PasswordInput)
    age = forms.IntegerField(label='age',min_value=1,max_value=150,)


def lo(request):
    if 'username' in request.session:
        return redirect('admi:home')
    elif request.method == "POST":
        n = request.POST['name']
        p = request.POST['password']
        if AdmiLogin().admin_auth(Aname = n,Apass = p):
            request.session['username'] = n
            return redirect('admi:home')
        return render(request,'admi/login.html',{'form':AdmiLoginForm(),'msg':"invalid credentiels"})
    return render(request,'admi/login.html',{'form':AdmiLoginForm()})

def home(request):
    if 'username' in request.session:
        q = Userdata.objects.all()
        return render(request,'admi/home.html',{'obj':q})
    return redirect('admi:login')
def delete(request,value):
    if Userdata.objects.filter(id = value).count() > 0:
        c = Userdata.objects.get(id = value)
        c.delete()
    return redirect('admi:home')


def add(request):
    if 'username' in request.session:
        action = "<form action=\"\" method=\"post\">"
        submit = "<button><input type=\"submit\"></button>"
        if request.method == 'POST':
            name = request.POST['name']
            password = request.POST['password']
            age = request.POST['age']
            Userdata.objects.create(uname = name, upassword = password, age = age)
            return redirect('admi:home')
        qr = Userdata.objects.all()
        context = {'obj':qr,'button':submit,'form':UserdataForm(),'action':action}
        return render(request,'admi/home.html',context)
    return redirect('admi:login')  

 
def edit(request):
    if 'username' in request.session:
        if request.method == 'POST':
            ide = request.POST['id']
            names = request.POST['name']
            passwords = request.POST['password']
            ages = request.POST['age']
            qu = Userdata.objects.get(id = ide)
            qu.uname = names
            qu.upassword = passwords  
            qu.age = ages 
            qu.save()
        return redirect('admi:home')
    return redirect('admi:login')
def ideees(request,value):
    if 'username' in request.session:
        submit = "<button class = \"btn-primary\"><input type=\"submit\" value = \"\">update</button>"
   
        ids = value 
        qu = Userdata.objects.get(id = ids)
        x = qu.upassword
        q = Userdata.objects.all()
        return render(request,'admi/home.html',{'obj':q,'qu':ids,'button2':submit,'formup': UserdataForm(initial={'age':qu.age,'password':x,'name':qu.uname})})
    return redirect('admi:login')
    
    

def lout(request):
    if 'username' in   request.session:
        request.session.flush() 
    return redirect('admi:login')

def userlogin(request):
    if 'user_username' in request.session:
        return redirect('admi:user_home')
    elif request.method == "POST":
        n = request.POST['name']
        p = request.POST['password']
        if Userdata().user_auth(Aname = n,Apass = p):
            request.session['user_username'] = n
            return redirect('admi:dashboard')
        return render(request,'admi/userlogin.html',{'form':UserdataForm(),'msg':"invalid credentiels"})
    return render(request,'admi/userlogin.html',{'form':UserdataForm()})

def user_home(request):
    if 'user_username' in request.session:
        return render(request,'admi/user_home.html',)
    return redirect('admi:userlogin')

def userlout(request):
    if 'user_username' in   request.session:
        request.session.flush() 
    return redirect('admi:userlogin')

def sign_up(request):
    if request.method == "POST":
        n = request.POST['name']
        p = request.POST['password']
        #a = request.POST['age'] 
        cn = request.POST['cpassword']
        if p == cn:
            if Userdata.objects.filter(uname = n).count():
                return render(request,'admi/sign.html',{'form':Sign(),'msg':"user_name already exist"})
            o = Userdata.objects.create(uname = n, upassword = p,age = 16 )
            o.save()
            return redirect('admi:dashboard')  
        else:
            return render(request,'admi/sign.html',{'form':Sign(),'msg':"password does not match"})
   
    return render(request,'admi/sign.html',{'form':Sign()})

def dashboard(request):
    if 'user_username' in request.session:
        products = Product.objects.all().filter(is_available = True)
    

        context = {'products':products}
        return render(request,'home.html',context)
    return redirect('admi:userlogin')