from django.urls import path

from . import views

urlpatterns = [
    path('login1/', views.login, name='login1'),

]
