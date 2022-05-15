from django.db import models

# Create your models here.

# Create your models here.
class AdmiLogin(models.Model):
    name = models.CharField(max_length=254)
    password = models.CharField(max_length=16)
    
    def __str__(self):
        return f"{self.name} {self.password}"

        
    def admin_auth(self,Aname,Apass):
        k = AdmiLogin.objects.filter(name = Aname).count()
        if k:
            q = AdmiLogin.objects.get(name = Aname)
            if q.password == Apass:
                return True

        else:
            return False

class Userdata(models.Model):
    uname = models.CharField(max_length=254)
    upassword =  models.CharField(max_length=16)
    age = models.IntegerField()

    def user_auth(self,Aname,Apass):
        k = Userdata.objects.filter(uname = Aname).count()
        if k:
            q = Userdata.objects.get(uname = Aname)
            if q.upassword == Apass:
                return True

        else:
            return False