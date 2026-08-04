from django.urls import path
from . import views


app_name ="favorites"

urlpatterns = [
    path(
    "recently-viewed/",
    views.recently_viewed,
    name="recently_viewed",
),
]