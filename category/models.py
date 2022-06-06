
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here. 
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True)#url
    description = models.TextField(max_length=100,blank = True)
    cat_image = models.ImageField(upload_to = 'photos/category',blank = True)
    #to change table name from defualt Categorys 
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse ('products_by_category', args = [self.slug]) #this function brings the slug/url of object
   
    def __str__(self):
        return self.category_name
