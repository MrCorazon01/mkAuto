from django import forms
from .models import ProfileModel
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    fullname = forms.CharField(label="Nom complet", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Veuillez entrer votre nom', 'name': 'fullname'}))
    username = forms.CharField(label="Nom utilisateur", max_length=100,  widget=forms.TextInput(attrs={'placeholder': 'Veuillez entrer votre username', 'name': 'username'}))
    email = forms.EmailField(label="Email", max_length=254, widget=forms.TextInput(attrs={'placeholder': 'Veuillez entrer votre email', 'name': 'email'}))
    password = forms.CharField(label="Mot de passe", max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Veuillez entrer votre mdp', 'name': 'password'}))
    password2 = forms.CharField(label="Confirmation mot de passe", max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe', 'name': 'password2'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', "fullname"]
        

    

class ProfileForm(forms.ModelForm):
    telephone = forms.CharField(label="Numéro de téléphone", max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Veuillez entrer votre tel', 'name': 'telephone'}))
    adresse = forms.CharField(label="Adresse", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Veuillez entrer votre adresse', 'name': 'adresse'}))
    ville = forms.CharField(label="Ville", max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Veuillez entrer votre ville', 'name': 'ville'}))
    postal_code = forms.CharField(label="Code postal", max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Veuillez entrer votre code posatal', 'name': 'postal_code'}))
    pays = forms.CharField(label="Pays", max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Pays', 'name': 'pays'}))

    class Meta:
        model = ProfileModel
        fields = ['telephone', 'ville', 'pays', 'postal_code', 'adresse']
        