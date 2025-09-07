from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import FeedbackForm 

from django.urls import reverse

def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.nom = request.user.username
            else:
                feedback.nom = "Inconnu"
            feedback.save()
            return redirect("merci")
    else:
        form = FeedbackForm()
    return render(request, "feedback/feedback_form.html", {"form": form})

def merci_view(request):
    return render(request, "feedback/merci.html")

def feedback_footer_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.nom = request.user.username if request.user.is_authenticated else "Inconnu"
            feedback.save()
    # redirige vers la même page avec un petit paramètre pour afficher le message
    referer = request.META.get("HTTP_REFERER", "/")
    if "?" in referer:
        return redirect(referer + "&thanks=1")
    else:
        return redirect(referer + "?thanks=1")
