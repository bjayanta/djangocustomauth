from django.urls import path
from .views import Signin

urlpatterns = [
    path('', Signin.as_view(), name='account.signin'),
]