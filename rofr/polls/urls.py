from django.urls import path, include

from . import views

urlpatterns = [
    # User APIs
    path('register/', views.register, name="register"),
    path('available/', views.available_polls, name="available_polls"),
    path('attempt/<int:poll_id>', views.attempt_poll, name="attempt_poll"),


    # Admin APIs
    path('create/', views.create_poll, name="create_poll"),
    path('responses/', views.create_poll, name="get_responses"),

]