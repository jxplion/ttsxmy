from django.shortcuts import render

# Create your views here.
def register(request):
    return render(request, 'ttsx_user/register.html')


def login(request):
    return render(request, 'ttsx_user/login.html')