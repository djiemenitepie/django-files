from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('register/', views.register, name = 'register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('update/<int:todo3_id>/<str:status>/', views.update_todo3, name='update_todo3'),
    path('delete/<int:todo3_id>/', views.delete_todo3, name='delete_todo3'),

]

