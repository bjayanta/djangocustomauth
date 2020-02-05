from django.shortcuts import render
from django.views import View

# Home view
class Home(View):
    context = {}

    def get(self, request):
        return render(request, 'home.html', self.context)

    def post(self, request):
        pass