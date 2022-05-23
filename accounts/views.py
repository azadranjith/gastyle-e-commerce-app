from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages

from django.contrib import auth 

from django.contrib.auth.decorators import login_required

from carts.models import Cart,CartItem

from carts.views import _cart_id
# Create your views here.
def register(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Registration successful. ')

            return redirect('register')
    else:

        form = RegistrationForm()

    context = {
        'form':form
    }
    return render(request,'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            
            try:
               
                cart = Cart.objects.get(cart_id = _cart_id(request))

                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                print(is_cart_item_exists)
                #exp
                product_variation = []
                pro_var_id = []
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        product_variation.append(list(item.variations.all())) 
                        pro_var_id.append(item.id)
                    ex_var_list = []
                    id = []
                    user_cart_item = CartItem.objects.filter(user=user)
                    for item in user_cart_item:
                        existing_variation = item.variations.all() #by default it is query set
                        ex_var_list.append(list(existing_variation))#while append we make it to list
                        id.append(item.id)

                    for each_variation in product_variation:
                        if each_variation in ex_var_list:
                            index = ex_var_list.index(each_variation)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.save()
                        else:
                            index = product_variation.index(each_variation)
                            item_id = pro_var_id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.user = user
                            item.save() 
                    # for item in cart_item:
                    #     item.user = user
                    #     item.save()

            except:
              
                pass
            
            auth.login(request,user)
            return redirect('home')

        else:
            messages.error(request,'invalid login credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out ')
    return redirect('login')


@login_required(login_url = 'login')
def dashboard(request):
    return render(request,'dashboard.html')