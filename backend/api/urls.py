from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.ChatView.as_view(), name='chat'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
