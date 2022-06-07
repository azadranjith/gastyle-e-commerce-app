
from django.shortcuts import render, get_object_or_404,redirect
from carts.models import CartItem
from category.models import Category
from carts.views import _cart_id
from django.urls import reverse
#for paginator
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from store.forms import ReviewForm

from store.models import Product,ProductGallery, ReviewRating
from orders.models import OrderProduct
from django.db.models import  Q

from django.http import HttpResponse
from django.contrib import messages



from wishlist.models import WishlistItem,Wishlist
from wishlist.views import _wish_id
# Create your views here.
def store(request,category_slug = None,min=0,max=100000):
    categories = None

    all_products = None
    wlist = []
    try:
        if request.user.is_authenticated:
            wishlist_items = WishlistItem.objects.filter(user=request.user)
        else:
            wishlist = Wishlist.objects.get(wishlist_id=_wish_id(request))

            wishlist_items = WishlistItem.objects.filter(wishlist = wishlist)
        for items in wishlist_items:
            wlist.append(items.product.product_name)
    
        
    except Wishlist.DoesNotExist:  
        wishlist_items = None
    print(wlist)
    

    if category_slug != None:
        categories = get_object_or_404(Category,slug = category_slug)
        all_products = Product.objects.filter(category = categories, is_available = True, price__lte=max,price__gte=min)

        paginator = Paginator(all_products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = Product.objects.filter(category = categories, is_available = True, price__lte=max,price__gte=min).count
    else:
        
        all_products = Product.objects.filter(price__lte=max,price__gte=min).order_by('-modified_date')# included the not available
        paginator = Paginator(all_products,6) 
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = Product.objects.filter(price__lte=max,price__gte=min).count

    
    context = {
        'min':min,
        'max':max,
        'products':paged_products,
        'product_count':product_count,
        'wishes':wlist,
        'wishlist_items':wishlist_items, 
    }
    return render(request,'store/store.html',context)



def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug) # category__slug ref to category in product from there to the slug of the category
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product = single_product).exists() # 'cart__cart_id' ie compares with value in CartItem table on cart field __means to go to the foreign key field and check with value
        
    except Exception as e:
        raise e  
    if request.user.is_authenticated:
        try:
            
            order_product = OrderProduct.objects.filter(user = request.user,product = single_product).exists()  

        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None



    #review

    reviews = ReviewRating.objects.filter(product= single_product,status = True)


    #gallery

    product_gallery = ProductGallery.objects.filter(product = single_product)


    
    context = {
        'single_product':single_product,
        'in_cart':in_cart,
        'product_gallery':product_gallery,
        'order_product':order_product,
        'reviews':reviews,  

    }
    return render(request,'store/product_detail.html',context)

def search(request):
    print("hi")
    if 'keyword' in request.GET:
        print("hi")
        keyword = request.GET['keyword']
        products = Product.objects.order_by('product_name').filter(Q(product_name__icontains = keyword) | Q(description__icontains = keyword))
        product_count = products.count
    else:
        products = None
        product_count = 0
    context = {
        'products':products,
        'product_count':product_count
    }
    return render(request,'store/store.html',context)

def filter(request):
    min = None
    max = None
    if request.method == "POST":
        
        min = request.POST['from']
        max = request.POST['to']
     
    url = request.META.get('HTTP_REFERER')
    categories = Category.objects.all()
    for i in categories: 
        print(i)
        if '/category/'+ i.slug in url:
            print("re routed")
            return redirect('products_by_filter', category_slug = i.slug,min=min,max=max)     
            # return (store(request,category_slug=i.slug,min = min,max=max))  
            # return HttpResponse("the category is "+ i.slug)    

        
    return(store(request,min=min,max=max))
    




def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:

            reviews = ReviewRating.objects.get(user__id=request.user.id,product__id = product_id)
            form = ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,"thank you, Your review updated")
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()

                # data.subject = request.POST['subject']
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']

                data.ip = request.META.get('REMOTE_ADDR')

                data.product_id = product_id

                data.user_id = request.user.id

                data.save()  

                messages.success(request,"review submitted , thank you.")

                return redirect(url)



def new_arrivals(request,category_slug = None,min=0,max=100000):
    categories = None

    all_products = None
    wlist = []
    try:
        if request.user.is_authenticated:
            wishlist_items = WishlistItem.objects.filter(user=request.user)
        else:
            wishlist = Wishlist.objects.get(wishlist_id=_wish_id(request))

            wishlist_items = WishlistItem.objects.filter(wishlist = wishlist)
        for items in wishlist_items:
            wlist.append(items.product.product_name)
    
        
    except Wishlist.DoesNotExist:  
        wishlist_items = None
    print(wlist)
    
    

    if category_slug != None:
        categories = get_object_or_404(Category,slug = category_slug)
        all_products = Product.objects.filter(category = categories, is_available = True, price__lte=max,price__gte=min)

        paginator = Paginator(all_products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = Product.objects.filter(category = categories, is_available = True, price__lte=max,price__gte=min).count
    else:
        
        all_products = Product.objects.filter(price__lte=max,price__gte=min).order_by('created_date')# included the not available
        paginator = Paginator(all_products,6) 
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = Product.objects.filter(price__lte=max,price__gte=min).count

    
    context = {
        'min':min,
        'max':max,
        'products':paged_products,
        'product_count':product_count,
        'wishes':wlist,
        'wishlist_items':wishlist_items, 
    }
    return render(request,'store/store.html',context)

