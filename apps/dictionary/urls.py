from django.urls import path
from . import views

app_name = "dictionary"

urlpatterns = [
    path("", views.word_list, name="word_list"),
    path(
    "contribute/",
    views.contribute_word,
    name="contribute_word",
),

    path(
    "my-contributions/",
    views.my_contributions,
    name="my_contributions",
),

    path('favorites/',views.my_favorites,name='my_favorites'),
    path('review/<int:pk>/',views.review_contribution,name='review_contribution'),
    path(
    "<slug:slug>/favorite/",
    views.add_to_favorites,
    name="favorite_word",
),
    path(
    "<slug:slug>/rate/",
    views.rate_word,
    name="rate_word",
),
    path("<slug:slug>/remove-favorite/",views.remove_favorites,name="remove_favorite"),
    path(
    "<slug:slug>/comment/",
    views.add_comment,
    name="add_comment",
),
    path(
    "comment/<int:comment_id>/reply/",
    views.reply_comment,
    name="reply_comment",
),
    path(
    "comment/<int:comment_id>/edit/",
    views.edit_comment,
    name="edit_comment",
),
    path(
    "comment/<int:comment_id>/delete/",
    views.delete_comment,
    name="delete_comment",
),
    path(
    "comment/<int:comment_id>/like/",
    views.like_comment,
    name="like_comment",
),
    path(
    "comment/<int:comment_id>/report/",
    views.report_comment,
    name="report_comment",
),
    path("<slug:slug>/", views.word_detail, name="word_detail"),
    
]