from django.shortcuts import render , get_object_or_404 , redirect
from django.http import HttpResponse
from .models import Client , mesurClient
import datetime
from django.db.models import Q 
from .forms import clientforms , mesurClientforms
from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
"""
def index(request ):
    context = {
        'client': Client.objects.all(),
        'mesure': get_object_or_404(mesurClient , pk = 1)

        #"books": Book.objects.all().filter(title__startswith = "v")
        
    }
    return render(request , "tella/index.html" , context ) 
"""


@login_required
def serchClient(request): 
    q = request.GET.get("q", "").strip()
   
    if q:
        clients = Client.objects.filter(Q(name__icontains=q) & Q(user=request.user))
    else:
        clients = Client.objects.filter(user=request.user).order_by("-id")

    total_client = clients.count()

    return render(request, "tella/index.html", {"clients": clients, "q": q, "total_client": total_client})

    

@login_required
def mesur(request, Client_id ):
    client = get_object_or_404(Client, id=Client_id, user=request.user)
    
    mesurs = client.mesures.all()
    return render(request, "tella/mesures.html", {"client":client , "mesurs": mesurs ,  } )

@login_required
def add(request):
    if request.method == 'POST':
        form = clientforms(request.POST)

        if form.is_valid():
            client = form.save(commit= False)
            client.user = request.user
            client.save()
            return redirect("tella:index")
    else :
        form = clientforms()

    return render(request , "tella/client-form.html",{"form": form} ) 
 
@login_required
def addMesur(request , Client_id):
    client = get_object_or_404(Client ,id = Client_id)

    if request.method == 'POST':
        form = mesurClientforms(request.POST)

        if form.is_valid():
            mesurClient = form.save(commit=False)
            mesurClient.client = client
            mesurClient.save()
            return redirect("tella:mesur", Client_id=Client_id )
    else :
        form = mesurClientforms()

    return render(request , "tella/mesur-form.html",{"form": form  , "client": client} ) 

# client = get_object_or_404(Client, id=client_id, user=request.user)
 
 
@login_required
def editClient(request, Client_id):
    client = Client.objects.get(pk = Client_id ,user= request.user)

    if request.method == 'POST':
        form = clientforms(request.POST , instance=client)

        if form.is_valid():
            form.save()
            return redirect("tella:index")
    else :
        form = clientforms(instance=client)

    return render(request , "tella/client-modife.html",{"form": form} ) 

@login_required
def removeclient(request , Client_id):
    client = Client.objects.get(pk = Client_id ,user = request.user)
    client.delete()
    return redirect("tella:index")

# mesure 

@login_required
def editmesur(request, mesure_id):
    mesur = mesurClient.objects.get(pk = mesure_id)
    
 
    if request.method == 'POST':
        form = mesurClientforms(request.POST , instance=mesur)

        if form.is_valid():
            form.save()
            messages.success(request ,"bravo la modifiction avec succer") 
            return redirect("tella:mesur" ,Client_id = mesur.client.id)  
    else :
        form = mesurClientforms(instance=mesur)

    return render(request , "tella/mesures-modifier.html",{"form": form} ) 


@login_required
def removemesur(request , mesure_id):
    mesur = mesurClient.objects.get(pk = mesure_id )
    mesur.delete()
    messages.success(request ,"bravo supprimer avec succer") 
    return redirect("tella:mesur" ,Client_id = mesur.client.id)   

