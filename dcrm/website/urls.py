from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    # path('', views.login_user, name="login"),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
]
