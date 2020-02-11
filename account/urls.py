from django.urls import path

from .views import Signin, Signup, Signout, ActivateAccount

urlpatterns = [
    path('', Signin.as_view(), name='account.signin'),
    path('signout/', Signout.as_view(), name='account.signout'),
    path('signup/', Signup.as_view(), name='account.signup'),
    path('activate/<uidb64>/<token>', ActivateAccount.as_view(), name='account.activate'),
]