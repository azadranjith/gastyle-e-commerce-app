
from django import forms

from store.models import Product


class ProductForm(forms.ModelForm):
    
    images = forms.ImageField(required=False,error_messages={'invalid':("Image files only ")},widget=forms.FileInput)  
    class Meta:
        model = Product
    
        fields= ['product_name','slug','description','price','images','stock','is_available','category']
    def __init__(self,*args,**kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
             self.fields[field].widget.attrs['class'] = 'form-control'  