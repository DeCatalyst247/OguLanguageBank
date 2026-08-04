from django.urls import path

from . import views

app_name = "culture"

urlpatterns = [

    path(
        "",
        views.culture_home,
        name="home",
    ),

    path(
        "articles/",
        views.article_list,
        name="article_list",
    ),

    path(
        "articles/<slug:slug>/",
        views.article_detail,
        name="article_detail",
    ),
    path(
        "proverbs/",
        views.proverb_list,
        name="proverb_list",
),

    path(
        "proverbs/<int:pk>/",
        views.proverb_detail,
        name="proverb_detail",
),

]