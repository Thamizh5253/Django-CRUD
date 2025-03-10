from django.urls import path
from .views import login_user, logout_user ,register_user ,google_oauth_login
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
     
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('get-token/', obtain_auth_token, name='get_token'),
    path('register/', register_user, name='register'),
    path('google-login/google-oauth2/', google_oauth_login, name='google_oauth_login'),


]

