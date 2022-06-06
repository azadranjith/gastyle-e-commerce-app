

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from orders.views import payment
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile  
from django.contrib import messages

from django.contrib import auth 

from django.contrib.auth.decorators import login_required

from carts.models import Cart,CartItem
import requests

from carts.views import _cart_id

from orders.models import Order, OrderProduct

#verification

from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.utils.encoding import force_bytes 

from django.contrib.auth.tokens import default_token_generator

from django.core.mail import EmailMessage  


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

            #user activation

            current_site = get_current_site(request)

            mail_subject = 'Please activate your account'

            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })

            to_email = email

            send_email = EmailMessage(mail_subject,message,to=[to_email])

            send_email.send()   

            
            messages.success(request,'thank you for registering please verify your email')

            return redirect('login')    

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
            
            auth.login(request,user)         #while checking out without login it prompts login page with next key(wich has the previous url after ?next where we came and ie next want go there next) on url 
           
               #to go to REFERER (parent url) we need to use requests lib (pip install requests)

            url = request.META.get('HTTP_REFERER')

           
            #install requests lib
            try:
                query = requests.utils.urlparse(url).query
         
                #print(query)
                # we get this next=/cart/checkout/


                params = dict(x.split('=') for x in query.split('&')) #split the '=' and made next as a key and rest as value 
            
                
                # print( params)
                # {'next': '/cart/checkout/'}


                if 'next' in params:
                    next_page = params['next']
                    return redirect (next_page)
            except:
                
                return redirect('dashboard') 

        else:
            messages.error(request,'invalid login credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    unpayed_order = Order.objects.filter(user = request.user,is_ordered = False) 
    unpayed_order.delete()
    auth.logout(request)
    messages.success(request,'you are logged out ')
    return redirect('login')


@login_required(login_url = 'login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user = request.user,is_ordered = True)


    orders_count = orders.count()
    
    

    user_profile = UserProfile.objects.get(user=request.user)

    # if not user_profile.profile_picture:

    #     user_profile.profile_picture = 
   
    context = {
        'orders_count':orders_count,
        'user_profile':user_profile,
    }
    return render(request,'accounts/dashboard.html',context)


@login_required(login_url='login')  
def my_orders(request):
    orders = Order.objects.order_by('-created_at').filter(user = request.user,is_ordered = True)

    orders_count = orders.count()

    context = {
        'orders_count':orders_count,
        'order_data':orders
    }
    return render(request,'accounts/my_orders.html',context)  



@login_required(login_url='login')  
def edit_profile(request):
    
    userprofile = get_object_or_404(UserProfile,user=request.user)
      

    
    print("hello")
    if request.method == 'POST':

        user_form = UserForm(request.POST,instance=request.user)#passing this instance bcz we are editing this form ,,ie to update the profile without creating a new one

        profile_form = UserProfileForm(request.POST,request.FILES,instance=userprofile) #request.FILES is for uploading file

        if user_form.is_valid() and profile_form.is_valid():
            
            user_form.save()
        
            profile_form.save()
    

            messages.success(request,'Your profile has been updated')
            return redirect('edit_profile')   
    else:
        user_form = UserForm(instance=request.user)

        profile_form = UserProfileForm(instance=userprofile)
    context = {
            'user_form': user_form,
            'profile_form':profile_form,
            'userprofile':userprofile,
        }
    return render(request,'accounts/edit_profile.html',context)


@login_required(login_url='login')   
def change_password(request):

    if request.method == "POST":
        
        current_password = request.POST['current_password']

        new_password = request.POST['new_password']

        confirm_password = request.POST['confirm_password']

        if new_password == confirm_password:  

            user = auth.authenticate(email=request.user.email,password = current_password)
            #standerd way is success = current_user.check_passsword(current_passsword)

            if user is not None:
                print('it worked')
                current_user = Account.objects.get(email=request.user.email)
                current_user.set_password(new_password)  
                current_user.save()     
                messages.success(request,'password updated')
                       
            else:
                messages.error(request,'confirm your current password')
                return redirect('change_password')  
        else:
            messages.error(request,'Password does not match')
            return redirect('change_password') 


    return render(request,'accounts/change_password.html')

def order_detail(request,order_id):

    order_detail = OrderProduct.objects.filter(order__order_number=order_id)#we are getting order number from Order table via __ bcz oder is ForiegnKey of Order table

    order = Order.objects.get(order_number=order_id)  

    subtotal = 0 
    for i in order_detail:
        
        subtotal += i.product_price * i.quantity 

    context = {
        'order_detail':order_detail,
        'order':order,
        'subtotal':subtotal
    }
    return render(request,'accounts/order_detail.html',context)  


def activate(request,uidb64,token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True

        user.save()

        messages.success(request,'your account is activated ')

        user_pro = UserProfile.objects.create(user = user)

        user_pro.save()  

        return redirect('login')

    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']

        if Account.objects.filter(email = email).exists():

            user = Account.objects.get(email = email)

            #RESET PASSWORD  

            current_site = get_current_site(request)

            mail_subject = 'Please Reset your password'

            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })

            to_email = email

            send_email = EmailMessage(mail_subject,message,to=[to_email])

            send_email.send()  

            messages.success(request,'password reset email has been sent to your registered email')
            return redirect('login')
   
        else:
            messages.error(request,'account with this email does not exist')
            return redirect('forgotPassword')  
    return render(request,'accounts/forgotPassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):

        request.session['uid'] = uid

        messages.success(request,'Please reset your password')

        return redirect('resetPassword')
    else:
        messages.error('this link is expired')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password =request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')

            user = Account.objects.get(pk=uid)  

            user.set_password(password)

            user.save()

            messages.success(request,'your password has been reseted ')
            return redirect('login')
        else:
            messages.error(request,'password do not match')
            return redirect('resetPassword')

    else:
        return render(request,'accounts/resetPassword.html')  