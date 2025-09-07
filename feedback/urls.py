from django.urls import path
from . import views

urlpatterns = [
    path("", views.feedback_view, name="feedback"),
    path("merci/", views.merci_view, name="merci"),
    path("feedback-footer/", views.feedback_footer_view, name="feedback_footer"),

]
