# accounts/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        TECHNICIAN = "TECHNICIAN", "Technician"

    # OneToOneField = each User gets EXACTLY one Profile
    # Like each person gets exactly one ID card
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    role = models.CharField(
        max_length=15,
        choices=Role.choices,
        default=Role.TECHNICIAN,  # Default is Technician (safer!)
    )

    # Extra info about the technician
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    avatar_initials = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return f"{self.user.username} — {self.get_role_display()}"

    # Helper properties to check role cleanly
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_technician(self):
        return self.role == self.Role.TECHNICIAN

    def save(self, *args, **kwargs):
        # Auto-generate initials from username if not set
        if not self.avatar_initials and self.user.username:
            self.avatar_initials = self.user.username[:2].upper()
        super().save(*args, **kwargs)


# --- SIGNALS ---
# A Signal is like a doorbell — when something happens (User created),
# it automatically rings another function (create_profile)
# This ensures every new User AUTOMATICALLY gets a Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """When a new User is created, automatically create their Profile."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """When a User is saved, also save their Profile."""
    instance.profile.save()
