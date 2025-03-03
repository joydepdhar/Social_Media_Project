from django.urls import path
from User_Auth import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('update/', views.update_user, name='update_user'),
    
]