from django.db import models
from django.contrib.auth.models import User


class ProfileModel(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #First_name et Last name se trouvent dans User qui est en relation OneToOneField avec user
    #email = models.EmailField(max_length=254) Se trouve dans le model User
    telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=100)
    ville = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    pays = models.CharField(max_length=50)
    

    def __str__(self):
        return f'{self.id}: {self.user.username}'
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        

class CarModel(models.Model):
    nom = models.CharField(max_length=200)
    couleur = models.CharField(max_length=200)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    carburant_consommation = models.DecimalField(max_digits=4, decimal_places=1)
    tech_surete = models.CharField(max_length=200)
    confort_conduit = models.CharField(max_length=200)
    espace_interieur = models.CharField(max_length=200)
    connectivite = models.CharField(max_length=200)
    image = models.ImageField(upload_to='car_images/')

    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = "Voiture"
        verbose_name_plural = "Voitures"

    
