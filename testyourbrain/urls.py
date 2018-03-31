from django.urls import path

from testyourbrain import views

urlpatterns=[
    path('testyourbrain', views.index, name='index')
]