"""ocrDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include

from ocr.views import *



urlpatterns = [
    path('', connexion, name = 'login'),
    # path('login', connexion, name = 'login'),
    path('register', inscription, name = 'register'),
    path('deconnexion', deconnexion, name = 'logout'),

    path('acceuil', index, name = 'acceuil'),
    path('upload/', upload, name = 'upload'),
    path('read/<str:data>/', read, name = 'read'),
    path('delete/<str:data>/', delete, name = 'delete'),


]
