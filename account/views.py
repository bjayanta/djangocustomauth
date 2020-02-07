from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# app
from .forms import CreateUserForm

# Signup view
class Signup(View):
    context = {
        'title': 'Sign UP'
    }

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        self.context['form'] = CreateUserForm()
        return render(request, 'signup.html', self.context)

    def post(self, request):
        self.context['form'] = CreateUserForm(request.POST)
        if self.context['form'].is_valid():
            self.context['form'].save()

            user = self.context['form'].cleaned_data.get('username')
            messages.success(request, 'Account is created for ' + user)

            return redirect('account.signin')

        return render(request, 'signup.html', self.context)


# Signin view
class Signin(View):
    context = {
        'title': 'Sign In'
    }

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        
        return render(request, 'signin.html', self.context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Username or Password is incorrect.')
            return render(request, 'signin.html', self.context)


# Signout view
class Signout(View):
    def get(self, request):
        logout(request)
        return redirect('account.signin')

    def post(self, request):
        pass