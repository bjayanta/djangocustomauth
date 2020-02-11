from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User

# app
from .forms import CreateUserForm
from .utils import generate_token

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
            user = self.context['form'].save()

            # set active status for the user
            user.refresh_from_db()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            email_subject = 'Active your account'
            my_email_messages = render_to_string('activate.html', {
                'user': user,
                'domail': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })

            email_message = EmailMessage(
                email_subject,
                my_email_messages,
                settings.EMAIL_HOST_USER,
                [user.email],
            )

            email_message.send()

            email = self.context['form'].cleaned_data.get('email')

            # messages.success(request, 'Account is created for ' + user)
            messages.success(request, 'You\'re Almost Done... A verification email was sent to: ' + email + '. Open this email and click the link to activate your account.')

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
        # return view
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
            return render(request, 'signin.html', status=401, context=self.context)


# Signout view
class Signout(View):
    def get(self, request):
        logout(request)
        return redirect('account.signin')

    def post(self, request):
        pass


# Activate Account view
class ActivateAccount(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully.')

            return redirect('account.signin')
        else:
            return render(request, 'activate_fail.html', status=401)
