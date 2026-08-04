from django.contrib import admin

# Register your models here.
from .models import ContactMessage
from django.utils import timezone

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (

        "name",

        "email",

        "subject",

        "is_read",

        "created_at",

    )


    actions = (
        "approve_selected",
        "reject_selected",
    )
    def approve_selected(self, request, queryset):
      '''  queryset.update(
            status=ContactMessage.Status.PUBLISHED,
            approved_by=request.user,
            approved_at=timezone.now(),
        )

    approve_selected.short_description = "Approve selected message"
    '''


    def reject_selected(self, request, queryset):
        queryset.update(
            status=Word.Status.DRAFT,
        )

    reject_selected.short_description = "Reject selected message"


    


    list_filter = (

        "is_read",

    )

    search_fields = (

        "name",

        "email",

        "subject",

    )