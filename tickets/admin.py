from django.contrib import admin
from .models import Ticket


# Register your models here.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    # Wich columns to show in the list view
    list_display = [
        "title",
        "machine_name",
        "priority",
        "status",
        "maintenance_type",
        "reported_by",
        "created_at",
    ]

    # Add filter sidebar on the right
    list_filter = ["status", "priority", "maintenance_type"]

    # Make the list searchable
    search_fields = ["title", "machine_name", "description"]

    # Show newest first
    ordering = ["-created_at"]
