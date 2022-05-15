
from django.shortcuts import render, get_object_or_404
from category.models import Category

from store.models import Product

# Create your views here.
def store(request,category_slug = None):
    categories = None

    all_products = None

    if category_slug != None:
        categories = get_object_or_404(Category,slug = category_slug)
        all_products = Product.objects.filter(category = categories, is_available = True)
        product_count = Product.objects.filter(category = categories, is_available = True).count
    else:
        all_products = Product.objects.all()# included the not available
        product_count = Product.objects.all().count
    context = {
        'products':all_products,
        'product_count':product_count   
    }
    return render(request,'store/store.html',context)



def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug) # category__slug ref to category in product from there to the slug of the category
    except Exception as e:
        raise e  
    context = {
        'single_product':single_product
    }
    return render(request,'store/product_detail.html',context)

