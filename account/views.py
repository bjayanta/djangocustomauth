from django.shortcuts import render
from django.views import View

# Signin view
class Signin(View):
    context = {
        'title': 'Signin'
    }

    def get(self, request):
        return render(request, 'signin.html', self.context)

    def post(self, request):
        pass