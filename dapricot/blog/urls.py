from django.urls import path

from dapricot.blog import views

app_name = 'dablog'

urlpatterns = [
    path('', views.postList, name='main_list'),
    path('p<int:page>', views.postList, name='main_list'),
    
    path('<int:year>', views.datePostList, name='date_filter_posts'),
    path('<int:year>/', views.datePostList, name='date_filter_posts'),
    path('<int:year>/p<int:page>', views.datePostList, name='date_filter_posts'),
    path('<int:year>/<int:month>', views.datePostList, name='date_filter_posts'),
    path('<int:year>/<int:month>/', views.datePostList, name='date_filter_posts'),
    path('<int:year>/<int:month>/p<int:page>', views.datePostList, name='date_filter_posts'),
    path('<int:year>/<int:month>/<int:day>', views.datePostList, name='date_filter_posts'),
    path('<int:year>/<int:month>/<int:day>/', views.datePostList, name='date_filter_posts'),
    path('<int:year>/<int:month>/<int:day>/p<int:page>', views.datePostList, name='date_filter_posts'),
    
    path('<int:year>/<int:month>/<int:day>/<slug:slug>', views.post, name='post'),
    
    path('<slug:filter_name>/', views.filterList, name='filter_list'),
    path('<slug:filter_name>/p<int:page>', views.filterList, name='filter_list'),
    
    path('<slug:filter_name>/<slug:value>/', views.postList, name='filter_posts'),
    path('<slug:filter_name>/<slug:value>/p<int:page>', views.postList, name='filter_posts'),
    
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
]