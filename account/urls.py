from django.urls import path
from .views import Signin, Signup, Signout

urlpatterns = [
    path('', Signin.as_view(), name='account.signin'),
    path('signout/', Signout.as_view(), name='account.signout'),
    path('signup/', Signup.as_view(), name='account.signup'),
]