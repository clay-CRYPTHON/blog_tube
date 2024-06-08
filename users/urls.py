from .views import *
from django.urls import path

urlpatterns = [
    path('login/', log_in, name="login"),
    path('be_author/', be_author, name="be_author"),

]