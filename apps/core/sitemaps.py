from django.contrib.sitemaps import Sitemap

from apps.dictionary.models import Word

from apps.learning.models import Lesson

from apps.culture.models import CultureArticle


class WordSitemap(Sitemap):

    changefreq = "weekly"

    priority = 0.9

    def items(self):

        return Word.objects.filter(
            status="published",
        )

    def lastmod(self, obj):

        return obj.updated_at


class LessonSitemap(Sitemap):

    changefreq = "weekly"

    priority = 0.8

    def items(self):

        return Lesson.objects.filter(
            is_published=True,
        )

    def lastmod(self, obj):

        return obj.updated_at


class ArticleSitemap(Sitemap):

    changefreq = "monthly"

    priority = 0.7

    def items(self):

        return CultureArticle.objects.filter(
            published=True,
        )

    def lastmod(self, obj):

        return obj.updated_at