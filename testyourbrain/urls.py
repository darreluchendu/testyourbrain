from django.urls import path

from testyourbrain import views

urlpatterns=[
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('session/<int:id>/', views.session, name='session'),
    path('register/', views.register, name='register'),
    path('new_game/', views.add_game, name='add_game')
  ]
