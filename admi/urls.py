from . import views
from django.urls import path


from . import views

app_name = 'admi'

urlpatterns = [

    path('signup',views.sign_up,name='sign_up'),
    path('userlogin/',views.userlogin,name = 'userlogin'),
    path('userlout/',views.userlout,name="userlout"),
    path('',views.lo,name = 'login'),
    path('home/',views.home,name='home'),
    path('user_home/',views.user_home,name='user_home'),
    path('<str:value>',views.delete,name='delete'),
    path('add/',views.add,name='add'),
    path('edit/',views.edit, name='edit'),
    path('lout/',views.lout,name="lout"),
    path('ideees/<int:value>',views.ideees,name = 'ideees'),
    path('dashboard/',views.dashboard,name='dashboard')
]