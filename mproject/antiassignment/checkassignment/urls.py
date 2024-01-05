
from django.contrib import admin
from django.urls import path
from checkassignment import views

urlpatterns = [
    
    path('',views.index,name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.student_login, name='login'),
    path('compare_form/', views.compare_form, name='compare_form'), 
    #path('compare_result/', views.compare_form, name='compare_result'), 
    
]