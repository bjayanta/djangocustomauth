from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# Home view
class Home(LoginRequiredMixin, View):
    context = {}
    login_url = '/account/'
    # redirect_field_name = 'next'

    def get(self, request):
        return render(request, 'home.html', self.context)

    def post(self, request):
        pass