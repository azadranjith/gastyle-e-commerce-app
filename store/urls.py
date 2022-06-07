from django.urls import path

from . import views
urlpatterns = [
    path('',views.store,name = 'store'),
    path('category/<str:category_slug>/<int:min>/<int:max>/',views.store,name = 'products_by_filter'),   
    path('category/<slug:category_slug>/',views.store,name = 'products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),

    ##
    path('filter/',views.filter,name='filter'), 


    path('submit_review/<int:product_id>',views.submit_review,name='submit_review'),

    path('new_arrivals/',views.new_arrivals,name='new_arrivals'),
    
]