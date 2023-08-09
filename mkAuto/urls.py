from django.urls import path
from .views import *


urlpatterns = [
    path('modele/<int:car_id>/', car_detail, name="modele"),
    
    path('profile/', view_profile, name='profile'),
    path('signup/', view_signup, name='signup'),
    path('signup2/', view_signup2, name='signup2'),
    path('register/', view_register, name="register"),
    path('register_part2/', view_register_part2, name="register_part2"),

    path('log/', view_log, name="log"),
    path('login/', view_login, name="login"),
    path('process_login/', process_login, name='process_login'),
    path('logout/', view_logout, name='logout'),


] 
