# tickets/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Ticket

from .forms import TicketForm  # We'll create this next!


# @login_required is a "decorator" - think of it as a BOUNCER at a club door
# If you're not logged in, it sends you to the login page automatically
@login_required
def ticket_list(request):
    """Show all tickets - with optional filtering."""

    # Start with ALL tickets
    tickets = Ticket.objects.all()

    # --- FILTERING ---
    # If the user clicked a filter button, the URL will have
    # something like ?status=OPEN or ?priority=HIGH
    # request.GET is a dictionary of those URL parameters

    status_filter = request.GET.get("status", "")  # '' means "no filter"
    priority_filter = request.GET.get("priority", "")
    type_filter = request.GET.get("type", "")

    if status_filter:
        tickets = tickets.filter(status=status_filter)
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)
    if type_filter:
        tickets = tickets.filter(maintenance_type=type_filter)

    # Count tickets by status (for the summary cards at the top)
    context = {
        "tickets": tickets,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "type_filter": type_filter,
        # Stats for summary cards
        "total_count": Ticket.objects.count(),
        "open_count": Ticket.objects.filter(status="OPEN").count(),
        "in_progress_count": Ticket.objects.filter(status="IN_PROGRESS").count(),
        "critical_count": Ticket.objects.filter(priority="CRITICAL").count(),
    }

    # render() = "take this data (context) and fill in this template"
    return render(request, "tickets/ticket_list.html", context)


@login_required
def ticket_detail(request, pk):
    """Show details for ONE specific ticket."""

    # get_object_or_404: try to find ticket with this ID
    # If it doesn't exist, show a "404 Not Found" page automatically
    ticket = get_object_or_404(Ticket, pk=pk)

    return render(request, "tickets/ticket_detail.html", {"ticket": ticket})


@login_required
def ticket_create(request):
    """Show a form to create a new ticket."""

    # HTTP has two main "methods":
    # GET  = "just show me the empty form"
    # POST = "I filled in the form and I'm submitting it"

    if request.method == "POST":
        # User submitted the form - process it
        form = TicketForm(request.POST)

        if form.is_valid():
            # Don't save to DB yet (commit=False)
            # because we need to add reported_by first
            ticket = form.save(commit=False)
            ticket.reported_by = request.user  # The logged-in user
            ticket.save()

            # Show a success notification
            messages.success(
                request, f'✅ Ticket "{ticket.title}" created successfully!'
            )
            # Redirect to the ticket's detail page
            return redirect("ticket_detail", pk=ticket.pk)
    else:
        # GET request - just show an empty form
        form = TicketForm()

    return render(
        request,
        "tickets/ticket_form.html",
        {
            "form": form,
            "title": "Report New Fault",
            "btn_label": "Submit Ticket",
        },
    )


@login_required
def ticket_edit(request, pk):
    """Edit an existing ticket."""

    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == "POST":
        # Pre-fill form with existing data, then overlay new data
        form = TicketForm(request.POST, instance=ticket)

        if form.is_valid():
            form.save()
            messages.success(request, f"Ticket updated successfully!")
            return redirect("ticket_detail", pk=ticket.pk)
    else:
        # Pre-fill the form with the ticket's current data
        form = TicketForm(instance=ticket)

    return render(
        request,
        "tickets/ticket_form.html",
        {
            "form": form,
            "ticket": ticket,
            "title": f"Edit: {ticket.title}",
            "btn_label": "Save Changes",
        },
    )


@login_required
def ticket_delete(request, pk):
    """Delete a ticket (only on POST for safety)."""

    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == "POST":
        title = ticket.title
        ticket.delete()
        messages.success(request, f'Ticket "{title}" deleted.')
        return redirect("ticket_list")

    # For GET, show a confirmation page
    return render(request, "tickets/ticket_confirm_delete.html", {"ticket": ticket})
