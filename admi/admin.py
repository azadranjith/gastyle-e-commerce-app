from django.contrib import admin

# Register your models here.
from .models import AdmiLogin, Userdata

admin.site.register(AdmiLogin)
admin.site.register(Userdata)