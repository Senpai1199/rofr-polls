from django.urls import path, include

from . import views

urlpatterns = [
    # User APIs
    path('register/', views.register, name="register"),
    path('available/', views.available_polls, name="available_polls"),
    path('attempt/<int:poll_id>', views.attempt_poll, name="attempt_poll"),


    # Admin APIs
    path('create/', views.create_poll, name="create_poll"),
    path('responses/<int:poll_id>/', views.get_poll_responses, name="get_poll_responses"),
    path('responses/download/<int:poll_id>/', views.poll_responses_excel, name="poll_responses_excel"),

    path('responses/<int:poll_id>/<int:q_id>/', views.get_question_responses, name="get_question_responses"),
    path('responses/download/<int:poll_id>/<int:q_id>', views.question_responses_excel, name="question_responses_excel"),
    path('responses/responses/aggregate/', views.aggregate_responses, name="aggregate_responses"),

]