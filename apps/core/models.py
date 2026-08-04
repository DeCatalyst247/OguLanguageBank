from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True




class ContactMessage(models.Model):

    name = models.CharField(
        max_length=150,
    )

    email = models.EmailField()

    subject = models.CharField(
        max_length=200,
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    is_read = models.BooleanField(
        default=False,
    )

    class Meta:

        ordering = (
            "-created_at",
        )

    def __str__(self):
        return self.subject