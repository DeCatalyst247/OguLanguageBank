import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.conf import settings
import dj_database_url

settings.DATABASES["default"] = dj_database_url.parse(
    os.environ["DATABASE_URL"],
    conn_max_age=600,
)

print("\nDATABASE ENGINE:", settings.DATABASES["default"]["ENGINE"])
print("\n--- PRODUCTION DATABASE INVENTORY ---")

from django.apps import apps

for model in apps.get_models():
    try:
        count = model.objects.count()
        print(f"{model._meta.label}: {count}")
    except Exception as e:
        print(f"{model._meta.label}: ERROR - {e}")