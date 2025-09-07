from django import forms
from .models import Client  , mesurClient

class clientforms(forms.ModelForm):
       class Meta:
        model = Client
        fields = ['name', 'numberPhone']
        labels = {'name':'nom','numberPhone':'numero'}
        widgets = {'numberPhone':
                   forms.TextInput(attrs={'type':'tel','placeholder':'+228 0000000'
              })} 

class mesurClientforms(forms.ModelForm): 
       class Meta:
        model = mesurClient
        fields = ['habit', 'panthalon']
        labels = {'habit':"habit",'panthalon':'panthalon'}
        widgets = {'habit':
                   forms.TextInput(attrs={'type':'tel','placeholder':"entrez les mesures de l'hablit EX: 34 45 23.. "
              })} 
        widgets = {'panthalon':
                   forms.TextInput(attrs={'type':'tel','placeholder':"entrez les mesures du  EX: 74 90 23.. "
              })} 

