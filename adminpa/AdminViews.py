from django .shortcuts import render


def admin_home(request):
    render(request,"adminpa/home.html")