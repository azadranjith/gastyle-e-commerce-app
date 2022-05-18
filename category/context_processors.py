
from category.models import Category

def menu_links(request):#takes a request and return dictionary 
    links = Category.objects.all()#to get all the categoies,,#it will bring all the category object list and store them in the 'links'variable

    return dict(links=links) 