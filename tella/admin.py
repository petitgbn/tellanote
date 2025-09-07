from django.contrib import admin
from .models import Client , mesurClient
# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'user')


@admin.register(mesurClient) 
class mesurClientAdmin(admin.ModelAdmin):

    list_display = ('client','habit','panthalon' ,'date')