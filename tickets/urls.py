from django.urls import path
from .views import base_page_view


# app_name lets us use "namespaced" URLs like tickets:list
# This avoids conflicts if two apps have a view with the same name

app_name = "tickets"


urlpatterns = [
    # /tickets/
]
