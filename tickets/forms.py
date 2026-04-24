# tickets/forms.py

from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    """
    ModelForm = a form that's automatically built from a Model.
    Like photocopying your Model blueprint to make a form!
    """

    class Meta:
        model = Ticket
        # Which fields to show in the form (we exclude reported_by
        # because we set that automatically in the view)
        fields = [
            "title",
            "machine_name",
            "location",
            "description",
            "priority",
            "status",
            "maintenance_type",
            "assigned_to",
            "scheduled_date",
        ]

        # widgets = customize how each field LOOKS in HTML
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Flash defect on Machine #1",
                }
            ),
            "machine_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Machine #1",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Gardner Facilities - Bay 3",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe the problem in detail...",
                }
            ),
            "priority": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "maintenance_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "scheduled_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",  # Shows a date picker in the browser!
                }
            ),
        }
