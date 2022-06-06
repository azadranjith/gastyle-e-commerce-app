import datetime

from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse

from carts.models import Cart,CartItem
from orders.models import Order, OrderProduct, Payment

from .forms import OrderForm


import json  


from store.models import Product
# Create your views here.
#for mail

from django.template.loader import render_to_string

from django.core.mail import EmailMessage  





def payment(request):  

    body = json.loads(request.body) 
    order = Order.objects.get(user=request.user,is_ordered = False,order_number = body['orderID'] )
   
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'], 
    
    )

    payment.save()  

    order.payment = payment

    order.is_ordered = True
    order.save()

    #move the cart_items ie ORDERED product to OrderProduct table

    cart_items = CartItem.objects.filter(user=request.user)

    print('these are the cart items you ordered ',cart_items)

    for item in cart_items:

        orderproduct = OrderProduct()
        print(item.quantity)

    #     #its a foreignkey so we can add order_id
        orderproduct.order_id = order.id

        orderproduct.payment = payment

        orderproduct.user_id = request.user.id

        orderproduct.product = item.product    

        orderproduct.quantity = item.quantity

        orderproduct.product_price = item.product.price

        orderproduct.ordered = True
    #       #you cannot just directly assign to many to many fields 

        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)

        product_variation = cart_item.variations.all()

        orderproduct = OrderProduct.objects.get(id = orderproduct.id)

        orderproduct.variations.set(product_variation)

         #fisrt save and then add variation
        orderproduct.save() 


    #reduce the quantity

       
        product = Product.objects.get(id = item.product.id)     

        product.stock -= item.quantity

        product.save()




    #remove the cart
        
    CartItem.objects.filter(user=request.user).delete()
   
    
        

    #send order recieved to customer
    mail_subject = 'Thank You for your order'

    message = render_to_string('orders/order_recieved_email.html',{
        'user':request.user,
        'order':order, 
      
    })

    to_email = request.user.email

    send_email = EmailMessage(mail_subject,message,to=[to_email])

    send_email.send()  
    #remove the cart


    #lecture 18 video 4


    #send order number and transaction id back to sendData method via Json response

    data = {
        'order_number':order.order_number,
        'transID' : payment.payment_id,
    }
    return JsonResponse(data)












def place_order(request,total=0,quantity=0):  

    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)

    cart_count = cart_items.count()

    print(cart_count)

    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0 

    tax = 0

    for cart_item in cart_items:

        total += (cart_item.quantity * cart_item.product.price)  
        quantity += cart_item.quantity
    
    tax = (3 * total)/100
    grand_total = total + tax

    if request.method == 'POST':

        form = OrderForm(request.POST)
        print("check")
        if form.is_valid():
            print("is valid")
            data = Order() #made an object of Order ie data

            data.user = current_user
            data.first_name = form.cleaned_data['first_name'] #this is how(cleaned_data) we take field values from request.post
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']

            data.order_total = grand_total

            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            # generate order number for that we append date with id of this order
            yr = int(datetime.date.today().strftime('%Y'))

            dt = int(datetime.date.today().strftime('%d'))

            mt = int(datetime.date.today().strftime('%m'))

            d = datetime.date(yr,mt,dt)

            current_date = d.strftime("%Y%m%d")
            #no default id is coming so
            order_number = current_date 

            data.order_number = order_number

            data.save()

            print(data.id)
            data.order_number += str(data.id)
            data.save()
            order_number = data.order_number
            order = Order.objects.get(user = current_user, is_ordered = False,order_number=order_number)

            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }
            return render(request,'orders/payment.html',context)  
        else:
            return redirect('checkout')   

def order_complete(request):

    order_number = request.GET.get('order_number')

    transID = request.GET.get('payment_id')

    print(order_number)
    print(transID) 
    try:
        
        
        order = Order.objects.get(order_number=order_number,is_ordered = True)
        
        ordered_products = OrderProduct.objects.filter(order_id = order.id)


        payment = Payment.objects.get(payment_id=transID)

        subtotal = 0

        for item in ordered_products:
            subtotal += item.product_price * item.quantity
       
        context = {
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID':payment.payment_id,
            'payment':payment,
            'subtotal':subtotal,
        }
        
        return render(request,'orders/order_complete.html',context)

    except (Payment.DoesNotExist,Order.DoesNotExist):

        return redirect('home')


        
