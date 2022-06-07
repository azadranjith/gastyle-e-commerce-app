
from dataclasses import fields
from django import forms
from category.models import Category
from orders.models import Order

from store.models import Product,Variation


class ProductForm(forms.ModelForm):
    
    images = forms.ImageField(required=False,error_messages={'invalid':("Image files only ")},widget=forms.FileInput)  
    class Meta:
        model = Product
    
        fields= ['product_name','description','price','images','stock','is_available','category']
    def __init__(self,*args,**kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'is_available':
                self.fields[field].widget.attrs['class'] = 'form-control'  

class CategoryForm(forms.ModelForm):
    cat_image = forms.ImageField(required=False,error_messages={'invalid':("Image files only ")},widget=forms.FileInput)  
    class Meta:
        model = Category
    
        fields= ['category_name','description','cat_image']  
    def __init__(self,*args,**kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields:
             self.fields[field].widget.attrs['class'] = 'form-control'  

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order

        fields = ['status']

    def __init__(self,*args,**kwargs): 
        super(OrderForm,self).__init__(*args,**kwargs)
        for field in self.fields:
             self.fields[field].widget.attrs['class'] = 'form-control'  
class VariationForm(forms.ModelForm):
    class Meta:
        model =Variation

        fields = ['product','variation_category','variation_value','is_active',]
    def __init__(self,*args,**kwargs):
        super(VariationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'is_active':
                self.fields[field].widget.attrs['class'] = 'form-control'  
