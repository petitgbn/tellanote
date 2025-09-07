from django.db import models
from django.contrib.auth.models import User


# Create your models here. user = models.ForeignKey(User, on_delete=models.CASCADE)  # 🔑 lien avec l’utilisateur
    
class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField( max_length=32 )
    numberPhone = models.CharField( max_length=50, blank=True)

    def __str__(self):
        return self.name


class mesurClient(models.Model):
    habit = models.CharField( max_length=150 ,blank=True)
    panthalon = models.CharField( max_length=150 ,blank=True)
    date = models.DateTimeField((""), auto_now=True, auto_now_add=False)
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE ,related_name='mesures') 
    


# python .\manage.py makemigrations

# python .\manage.py migrate 

# python .\manage.py createsuperuser

#  python .\manage.py runserver  

# petite  a@r.com     év"IIOM"OMZR(34)

# év"IIOM"OMZR(34)


# petitet  at@r.com

# év"IIOn"OMZR(34)
