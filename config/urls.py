"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from apps.core.sitemaps import (
    WordSitemap,
    LessonSitemap,
    ArticleSitemap,
)

admin.site.site_header = "Ogu Language Bank Administration"

admin.site.site_title = "OLB Admin"

admin.site.index_title = "Welcome to OLB Management System"
sitemaps = {

    "words": WordSitemap,

    "lessons": LessonSitemap,

    "articles": ArticleSitemap,

}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.core.urls')),
    path('dictionary/',include('apps.dictionary.urls')),
    path('accounts/',include('apps.accounts.urls')),
    path('learning/',include('apps.learning.urls')),
    path('quizzes/',include('apps.quiz.urls')),
    path('favorites/',include('apps.favorites.urls')),
    path(

    "sitemap.xml",

    sitemap,

    {

        "sitemaps": sitemaps,

    },

),
    path(
    "robots.txt",
    TemplateView.as_view(
        template_name="robots.txt",
        content_type="text/plain",
    ),
),
    path(
    "culture/",
    include("apps.culture.urls"),
),
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "apps.core.views.custom_404"

handler500 = "apps.core.views.custom_500"