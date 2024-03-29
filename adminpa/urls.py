from django.urls import path
from . import views,AdminViews
from .views import *


urlpatterns = [
    path("Cadmin/", views.adminLogin),
    path("demopage/", views.demopage, name="demopage"),
    path("demotemplate/", views.demotemplate, name="demotemplate"),
    # page  for cadm
    path("admin_home/", views.admin_home, name="admin_home"),
    path("add-product/", views.add_product, name="add_product"),
    path("product-list/", views.product_list, name="product_list"),
    path("edit-product/<id>", views.edit_product, name="edit_product"),
    path("add-category/", views.add_category, name="add_category"),
    path("category_list/", views.category_list, name="category_list"),
    path("edit-category/<id>", views.edit_category, name="edit_category"),
    path("delete-category/<id>", views.delete_category, name="delete_category"),
    path("delete-product/<id>", views.delete_product, name="delete_product"),
    path("accountlist/", views.accountlist, name="accountlist"),
]
