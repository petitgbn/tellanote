from django.urls import path
from . import views  

app_name ="tella"


urlpatterns = [
    path('', views.serchClient, name='index'),
    path('ajouter/', views.add, name='add'),
    
    path('mesure/<int:Client_id>' , views.mesur, name='mesur'),
    path('addMesur/<int:Client_id>' , views.addMesur, name='addMesur'),
    path('modifier-livre/<int:Client_id>/' , views.editClient , name= "edit-client"),
    path('supprimer-client/<int:Client_id>/', views.removeclient , name="supprimer-client"),

    path('modifer-mesur/<int:mesure_id>/', views.editmesur , name="modifer-mesur"),
    path('supprimer-mesur/<int:mesure_id>/', views.removemesur , name="supprimer-mesur"),
    
    
] # 3ApT7x&R5/bURkd
 
#    python .\manage.py runserver   

""""
django-environ
gunicorn
Pillow
psycopg2-binary
sqlparse
tzdata
whitenoise dj-database-url
Python 3.13.6

postgresql://teste_ihns_user:gVhXRDgrZwvkOGgcqRp5JcCiYkaLZ2qH@dpg-d2qvrul6ubrc73e1er60-a.oregon-postgres.render.com/teste_ihns

""" 