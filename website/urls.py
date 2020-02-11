from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import Home

urlpatterns = [
    path('', login_required(Home.as_view()), name='home'),
]