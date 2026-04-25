from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Think of each class as one LEGO blueprint


class Ticket(models.Model):
    # --- CHOICES (like a dropdown menu) ---
    # These are constants - we write them IN the class, at the top
    # FORMAT: ('value_stored_in_db', 'Human readable label')

    class Priority(models.TextChoices):
        LOW = "LOW", "low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In_Progress"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    class MaintenanceType(models.TextChoices):
        PREVENTIVE = "PREVENTIVE", "Preventive"
        CORRECTIVE = "CORRECTIVE", "Corrective"
        SCHEDULED = "SCHEDULED", "Scheduled"

    # --- FIELDS (the columns in our table) ---

    # The title of the problem - like the subject of an email
    title = models.CharField(max_length=200)

    # A longer description - no character limit
    description = models.TextField()

    # Wich machine is broken?
    machine_name = models.CharField(max_length=100)

    # Location in the facility
    location = models.CharField(max_length=100, blank=True)

    # Priority dropdown - defaults to MEDIUM if not specified
    priority = models.CharField(
        max_length=12,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    # Status dropdown - always starts as OPEN
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.OPEN,
    )

    # Type of maintenace needed
    maintenance_type = models.CharField(
        max_length=15,
        choices=MaintenanceType.choices,
        default=MaintenanceType.CORRECTIVE,
    )

    # WHO reported this? Links to Django's built-in User
    # on_delete=CASCADE means: if the user is deleted, delete their tickets too
    reported_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reported_tickets"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )

    # Timestamps - Django fills these in AUTOMATICALLY
    created_at = models.DateTimeField(auto_now_add=True)  # Set once, on creation
    update_at = models.DateTimeField(auto_now=True)  # Updates every time you save

    # Scheduled date for maintenance  (optional)
    scheduled_date = models.DateField(null=True, blank=True)


# --- META (extra setting for this model) ---
class Meta:
    # Default ordering: newest tickets first
    ordering = ["-created_at"]
    # Human-readable names for the admin panel
    verbose_name = "Ticket"
    verbose_name_plural = "Tickets"


# --- METHODS ---
# This is what shows up when you print a Ticket object
# Like a name tag for the object
def __str__(self):
    return f"[{self.priority}] {self.title} - {self.machine_name}"


# A helper property: is this  tickets urgent?
@property
def is_urgente(self):
    return self.property in [self.Priority.HIGH, self.Priority.CRITICAL]
