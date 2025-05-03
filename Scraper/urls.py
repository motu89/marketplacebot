from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views


urlpatterns=[


    path('', views.scraper, name='scraper'),
    path('account/<int:account_number>/', views.scraper_with_account, name='scraper_with_account'),
  
]