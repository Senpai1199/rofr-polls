from django.urls import path, include

from . import views

urlpatterns = [
    # User APIs
    path('register/', views.register, name="register"),
    path('available/', views.available_polls, name="register"),

    # Admin APIs
    path('create/', views.create_poll, name="create_poll"),
]