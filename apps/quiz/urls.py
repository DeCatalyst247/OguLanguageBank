from django.urls import path

from . import views

app_name = "quiz"

urlpatterns = [

    path(
        "",
        views.quiz_list,
        name="quiz_list",
    ),

    path(
        "<int:pk>/",
        views.quiz_detail,
        name="quiz_detail",
    ),

    path(
        "<int:pk>/result/",
        views.quiz_result,
        name="quiz_result",
    ),

    path(
        "history/",
        views.quiz_history,
        name="quiz_history",
    ),

]