from django.contrib import admin

# Register your models here.
from . models import Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)} #to automatically  get value typed in  category name to slug field at admin panel 

    list_display = ('category_name','slug') #display with cat name

admin.site.register(Category,CategoryAdmin)