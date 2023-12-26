from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def create_superuser(request):
    password = "testing321"
    if User.objects.filter(email='admin@giftos.com').exists():
        return redirect("homepage")
    User.objects.create_superuser(email='admin@giftos.com', password=password)
    user = User.objects.get(email='admin@giftos.com')
    user.set_password(password)
    user.save()
    return redirect("homepage")