from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import redirect, render , get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from tellaNote import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from . tokens import generateToken
# Create your views here.
 
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect


def home(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('tella:index')
    
    return render(request, 'authentification/index.html')




def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpwd = request.POST['confirmpwd']
        if User.objects.filter(username=username):
            messages.add_message(request,messages.ERROR, 'Ce nom d’utilisateur est déjà pris, veuillez en choisir un autre.')
            return render(request,'authentification/signup.html',{'messages':messages.get_messages(request)})
        #messages.error(request,'messages error') affiche le msg dans l'interface admin,il faut configurer dans l'interface utilisateurs
        if User.objects.filter(email=email):
            messages.add_message(request,messages.ERROR, 'Un compte existe déjà avec cet email')
            return render(request,'authentification/signup.html',{'messages':messages.get_messages(request)})
        if len(username)>100:
            messages.add_message(request,messages.ERROR, 'Please the username must not be more than 100 character.')
            return render(request,'authentification/signup.html',{'messages':messages.get_messages(request)})

        if len(password)<8:
            messages.add_message(request,messages.ERROR, 'Le mot de passe doit contenir au moins 8 caractères')
            return render(request,'authentification/signup.html',{'messages':messages.get_messages(request)})
        

        if len(username)<5:
            messages.add_message(request,messages.ERROR, 'Le nom d’utilisateur doit contenir au minimum 5 caractères..')
            return render(request,'authentification/signup.html',{'messages':messages.get_messages(request)})
        
        if not username.isalnum():
            messages.add_message(request,messages.ERROR, 'Le nom d’utilisateur doit être alphanumérique')
            return render(request,'authentification/signup.html',{'messages':messages.get_messages(request)})
                        

        if password != confirmpwd:
            messages.add_message(request,messages.ERROR, 'Les mots de passe ne correspondent pas ')
            return render(request,'authentification/signup.html',{'messages':messages.get_messages(request)})

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name =firstname
        my_user.last_name = username
        my_user.is_active = False
        my_user.save()
        messages.add_message(request,messages.SUCCESS, 'Votre compte a été créé avec succès. Nous vous avons envoyé un email. Vous devez le confirmer afin d’activer votre compte.')
# send email when account has been created successfully
        subject = "Bienvenue sur TELLA-NOTE"
        message = "Bienvenue " + my_user.first_name + " " + my_user.last_name + "Merci d’avoir choisi \n \nTella-Note,\n\n votre application de prise de mesures et d’organisation pour couturières.\n\nPour finaliser votre inscription, veuillez confirmer votre adresse e-mail.\n\nÀ très bientôt sur Tella-Note ✂️\n--\n L’équipe Tella-Note dont \n EMMANUEL AMEN"
        
        from_email = settings.EMAIL_HOST_USER
        to_list = [my_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

# send the the confirmation email 
        current_site = get_current_site(request) 
        email_suject = "Confirmation de votre email de Tella-Note"
        messageConfirm = render_to_string("emailConfimation.html", {
            'name': my_user.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(my_user.pk)),
            'token': generateToken.make_token(my_user)
        })       

        email = EmailMessage(
            email_suject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [my_user.email]
        )

        email.fail_silently = False
        email.send()
        return render(request,'authentification/signin.html',{'messages':messages.get_messages(request)})
    return render(request, 'authentification/signup.html')    

"""
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        my_user = get_object_or_404(User ,username=username)
        #my_user = User.objects.get(username=username)


        if user is not None:
            login(request, user)
            
            return redirect('tella:index')
        elif my_user.is_active == False:
            messages.add_message(request,messages.ERROR, 'you have not confirm your  email do it, in order to activate your account')
            return render(request,'authentification/signin.html')
        else:
            messages.add_message(request,messages.ERROR, 'bad authentification')
            return render(request,'authentification/signin.html',{'messages':messages.get_messages(request)})
    
    else :

        return render(request, 'authentification/signin.html') """

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # utilisateur valide ET mot de passe correct
            if user.is_active:
                login(request, user)
                return redirect('tella:index')
            else:
                messages.error(request, "Vous devez d'abord activer votre compte par email.")
                return render(request, 'authentification/signin.html')

        else:
            # utilisateur introuvable OU mauvais mot de passe
            try:
                my_user = User.objects.get(username=username)
                if not my_user.is_active:
                    messages.error(request, "Vous devez confirmer votre email pour activer votre compte.")
                else:
                    messages.error(request, "Nom d’utilisateur ou mot de passe incorrect.")
            except User.DoesNotExist:
                messages.error(request, "Nom d’utilisateur ou mot de passe incorrect.")

            return render(request, 'authentification/signin.html')

    return render(request, 'authentification/signin.html')


def signout(request):
    logout(request)
    messages.success(request, 'logout successfully!')
    return redirect('authentification:home')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        my_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        my_user = None

    if my_user is not None and generateToken.check_token(my_user, token):
        my_user.is_active  = True        
        my_user.save()
        messages.add_message(request,messages.SUCCESS, "Votre compte a été activé. Vous pouvez maintenant vous connecter en remplissant le formulaire ci-dessous.")
        return render(request,"authentification/signin.html",{'messages':messages.get_messages(request)})
    else:
        messages.add_message(request,messages.ERROR, 'L’activation a échoué, veuillez réessayer')
        return render(request,'authentification/index.html',{'messages':messages.get_messages(request)})
