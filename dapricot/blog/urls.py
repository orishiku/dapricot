"""OrishikuDotCom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from . import views

app_name = 'dapricot_blog'


urlpatterns = [
    path('', views.postList, name='main_list'),
    path('<int:page>', views.postList, name='main_list'),
    path('<slug:filter_name>/', views.filterList, name='filter_list'),
    path('<slug:filter_name>/<int:page>', views.postList, name='filter_list'),
    path('<slug:filter_name>/<slug:value>', views.postList, name='filter_posts'),
    path('<slug:filter_name>/<slug:value>/<int:page>', views.postList, name='filter_posts'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>', views.post, name='post'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
]