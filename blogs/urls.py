from .views import *
from django.urls import path

urlpatterns = [
    path('', blogs, name="blogs"),
    path('category/<str:slug>/', blog_category, name="blog_category"),
    path('author/<uuid:uuid>/', author, name="author"),
    path('detail/<slug:slug>/', BlogDetailView.as_view(), name="blog_detail"),
    path('search/', search, name="search"),
    path('post/add', add_post, name="add_post"),
    path('post/<slug:slug>/edit/', edit_blog, name="edit_blog"),
    path('post/<slug:slug>/delete/', remove_blog, name="remove_blog"),

]
