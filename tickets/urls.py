# tickets/urls.py

from django.urls import path
from . import views

# app_name lets us use "namespaced" URLs like tickets:list
# This avoids conflicts if two apps have a view with the same name
app_name = "tickets"

urlpatterns = [
    # /tickets/
    path("", views.ticket_list, name="ticket_list"),
    # /tickets/create/
    path("create/", views.ticket_create, name="ticket_create"),
    # /tickets/1/   (the <int:pk> captures the number from the URL)
    path("<int:pk>/", views.ticket_detail, name="ticket_detail"),
    # /tickets/1/edit/
    path("<int:pk>/edit/", views.ticket_edit, name="ticket_edit"),
    # /tickets/1/delete/
    path("<int:pk>/delete/", views.ticket_delete, name="ticket_delete"),
]
