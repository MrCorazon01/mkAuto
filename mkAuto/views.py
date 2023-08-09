from django.shortcuts import render, redirect
from .forms import ProfileForm, UserForm
from django.contrib.auth.models import User
from .models import ProfileModel, CarModel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import (validate_password, 
UserAttributeSimilarityValidator, 
MinimumLengthValidator, 
CommonPasswordValidator, 
NumericPasswordValidator)
from django.core.exceptions import ValidationError



#----------------------------------------------------------------------------------
#                       La vue pour la partie modèle
#----------------------------------------------------------------------------------


#La vue pour gérer la sliding des voitures
def car_detail(request, car_id):
    car = CarModel.objects.get(id=car_id)
    next_car = CarModel.objects.filter(id__gt=car_id).order_by('id').first()
    previous_car = CarModel.objects.filter(id__lt=car_id).order_by('-id').first()
    context = {'car': car, 'next_car': next_car, 'previous_car': previous_car}

    return render(request, 'mkAuto/voiture.html', context)


#----------------------------------------------------------------------------------
#                       La vue pour la partie utilisateur anonyme
#----------------------------------------------------------------------------------


#La vue vers la page utilisateur anonyme
def view_log(request):
    return render(request, 'mkAuto/log.html')


#----------------------------------------------------------------------------------
#                       Les vues pour la partie inscription
#----------------------------------------------------------------------------------


#La vue vers la page d'inscription(elle est lié avec la vue *view_register*)
def view_signup(request):
    form1 = UserForm()
    form2 = ProfileForm()
    
    return render(request, "mkAuto/signup.html", {"form1": form1, 'form2': form2})


# Définition d'une classe pour personnalisé le message par défaut des validateur password dans view_register
class CustomPasswordValidator:
    def __init__(self, validators):
     self.validators = validators

    def validate(self, password, user=None):
        errors = []
        for validator in self.validators:
            try:
                validator.validate(password, user)
            except ValidationError as e:
                # Ajoute le message d'erreur personnalisé
                if isinstance(validator, UserAttributeSimilarityValidator):
                    e.message = "Le mot de passe ne doit pas contenir d'informations d'identification utilisateur."
                elif isinstance(validator, MinimumLengthValidator):
                    e.message = "Le mot de passe doit contenir au moins 8 caractères."
                elif isinstance(validator, CommonPasswordValidator):
                    e.message = "Le mot de passe est trop commun et facile à deviner."
                elif isinstance(validator, NumericPasswordValidator):
                    e.message = "Le mot de passe ne doit pas être uniquement numérique."
                errors.extend(e.error_list)
        if errors:
            raise ValidationError(errors)


#Process d'incription de la première page
def view_register(request):
    if request.method == 'POST':
        # Si la méthode HTTP est POST, on récupère les informations de la première page du formulaire d'inscription
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')

    try:
        #On vérifie si le nom utilisateur chosie n'existe pas déjà dans la base de donnée
        is_user = User.objects.get(username=username)
        form1 = UserForm(request.POST)  
        form2 = ProfileForm(request.POST)
        return render(request, 'mkAuto\signup.html', {'error_username': 'Le username choisi n\'est pas disponible', 'form1': form1, 'form2': form2})
    except User.DoesNotExist:

        #On splite le fullname ici parcequ'on avais utiliser les attributs first_name et last_name dans la classe User
        first_name = fullname.split()[0]
        last_name = ' '.join(fullname.split()[1:])

        try:
            # Vérifie la complexité du mot de passe en utilisant tous les validateurs (les 4 qu'on a vue dans la version actuelle)
            validate_password(
                password1,
                user=username,
                password_validators=[
                    CustomPasswordValidator([
                        UserAttributeSimilarityValidator(
                            user_attributes=("username",)),
                        MinimumLengthValidator(8),
                        CommonPasswordValidator(),
                        NumericPasswordValidator(),
                    ])
                ],
            )
        except ValidationError as e:
            # Si le mot de passe n'est pas valide, on affiche le message d'erreur correspondant

            # on redirige vers la première page du formulaire
            form1 = UserForm(request.POST)
            form2 = ProfileForm(request.POST)

            return render(request, 'mkAuto/signup.html', {"form1": form1, "form2": form2, 'error_message': e.messages})

        # On vérifie que les mots de passe correspondent
        if password1 != password2:
            # on redirige vers la première page du formulaire
            form1 = UserForm(request.POST)
            form2 = ProfileForm(request.POST)

            return render(request, 'mkAuto/signup.html', {"form1": form1, "form2": form2, 'error': 'Les deux mots de passe doivent être les mêmes.'})

        # On stocke les infos de l'utilisateur dans la session pour pouvoir les récupérer dans la deuxième page du formulaire (avec la vue view_register_part2)
        user_info = {'username': username, 'first_name': first_name, 'last_name': last_name,
                     'email': email, 'password': password1, 'telephone': telephone}
        request.session['user_info'] = user_info

        # On redirige vers la deuxième page du formulaire
        return redirect('register_part2')
    else:
        # Si la méthode HTTP est GET, on affiche la première page du formulaire d'inscription
        form1 = UserForm(request.POST)
        form2 = ProfileForm(request.POST)
        return render(request, 'mkAuto/signup.html', {"form1": form1, "form2": form2})


#La deuxième page de la formulaire d'inscription (lié avec la vue *view_register_part2*)
def view_signup2(request):
    return render(request, "mkAuto/signup2.html")

#Process d'inscription de la deuxième page
def view_register_part2(request):
    # On récupère les infos de l'utilisateur depuis la session
    user_info = request.session.get('user_info')

    if request.method == 'POST':
        # Si la méthode HTTP est POST, on récupère les informations de la deuxième page du formulaire d'inscription
        adresse = request.POST.get('adresse')
        ville = request.POST.get('ville')
        postal_code = request.POST.get('postal_code')
        pays = request.POST.get('pays')

        #On crée le User 
        user = User.objects.create_user(username=user_info['username'], first_name=user_info['first_name'],
                                        last_name=user_info['last_name'], email=user_info['email'], password=user_info['password'])
        #On crée ensuite l'utilisateur
        profile = ProfileModel.objects.create(
            user=user, telephone=user_info['telephone'], adresse=adresse, ville=ville, postal_code=postal_code, pays=pays)

        # On supprime les informations stockées dans la session
        del request.session['user_info']

        # On redirige vers la page de connexion pour qu'il puisse se connecter
        return redirect('login')
    #S'il y'a erreur dans les données saisies  
    else:
        form1 = UserForm(request.POST)
        form2 = ProfileForm(request.POST)
        if form1.is_valid():
            form1.save()
        else:
            form1 = UserForm()
        if form2.is_valid():
            form2.save()
        else:
            form2 = ProfileForm()
        # Si la méthode HTTP est GET, on affiche la deuxième page du formulaire d'inscription
        return render(request, 'mkAuto/signup2.html', {'form1': form1, 'form2': form2})


#----------------------------------------------------------------------------------
#                       Les vues pour la partie connexion
#----------------------------------------------------------------------------------


#Affiche la page de connexion
def view_login(request):
    return render(request, 'mkAuto/login.html')


#Affiche les informations de l'utilsateur si connecté et la page anonyme si non connecté
def view_profile(request):
    user = request.user
    if user.is_authenticated:
        try:
            profile = ProfileModel.objects.get(user=user)
        except ProfileModel.DoesNotExist:
            profile = None
        return render(request, 'mkAuto/profile.html', {'profile': profile})
    else:
        return redirect('log')


#Processus pour la partie connexion de la vue login
def process_login(request):
    form1=UserForm(request.POST)
    form2 = ProfileForm(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
    return render(request, 'mkAuto/login.html', {'error': 'Nom d\'utilisateur ou mot de passe incorrect.', 'form1': form1, 'form2': form2})


#----------------------------------------------------------------------------------
#                       La vue pour la partie déconnexion
#----------------------------------------------------------------------------------


def view_logout(request):
    logout(request)
    return redirect('login')





