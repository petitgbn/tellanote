from django.db import models

# Create your models here.

class Feedback(models.Model):
    nom = models.CharField(max_length=100, default="Inconnu")
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.date.strftime('%d/%m/%Y %H:%M')}"
