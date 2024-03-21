from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ProductForm
from store.models import Product
from .forms import CategoryForm
from category.models import Category

# Create your views here.
def demopage(request):
    return HttpResponse("demopage")


def demotemplate(request):
    return render(request, "adminpa/demo.html")


def adminLogin(request):
    return render(request, "adminpa/signin.html")


# def adminLogin(request):
#     if request.user.is_authenticated and request.user.is_superuser:
#         return redirect("admin_panel")

#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         print("email:", email, "password:", password)
#         user = authenticate(request, email=email, password=password)
#         if user and user.is_superuser:
#             print("its superuser")
#             login(request, user)
#             return redirect("admin_home")

    return render(request, "adminpa/signin.html")


def admin_home(request):
    return render(request, "adminpa/home.html")


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(product_list)
    form = ProductForm()
    return render(request, "adminpa/add_product.html", {"form": form})


def product_list(request):
    products = Product.objects.all()  # Assuming Product is your model
    return render(request, "adminpa/product_list.html", {"products": products})


def edit_product(request,id):
    product=Product.objects.get(id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect(product_list)
    form = ProductForm(instance=product)
    return render(request, "adminpa/add_product.html", {"form": form})


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect(category_list)
    form = CategoryForm()
    return render(request, "adminpa/add_category.html", {"form": form})


def edit_category(request, id):
    product = Category.objects.get(id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(category_list)
    form = CategoryForm(instance=product)
    return render(request, "adminpa/edit_category.html", {"form": form})


def category_list(request):
    category = Category.objects.all()  # Assuming Product is your model
    return render(request, "adminpa/category_list.html", {"categories": category})

def delete_product(request,id):
    products= Product.objects.get(id=id)
    products.delete()
    return redirect(product_list)


def delete_category(request, id):
    categories = Category.objects.get(id=id)
    categories.delete()
    return redirect(category_list)
