from django.contrib import admin

# Register your models here.

from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("nom", "message", "date")
    search_fields = ("nom", "message")
    list_filter = ("date",)
