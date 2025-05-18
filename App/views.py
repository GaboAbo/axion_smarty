"""
Views for the core 'App' module.

Includes:
- Entry and dashboard views
- Sidebar rendering
- PDF generation and emailing for maintenance orders
"""

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, JsonResponse

from .Constants.logo import OLYMPUS_LOGO
from Order.models import Order
from AuthUser.models import Engineer

from weasyprint import HTML
from premailer import transform
from io import BytesIO


def Index(request):
    """
    Entry view for the web app.

    Redirects authenticated users to the home dashboard,
    otherwise renders the index page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirect or rendered HTML page.
    """
    email = request.session.get("user_email")
    name = request.session.get("full_name")
    if name and email:
        return redirect("home")
    return render(request, 'index.html')


def HomeView(request):
    """
    Renders the main dashboard view.

    Context includes the authenticated user's name and email from session.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered dashboard page.
    """
    context = {
        "user_email": request.session.get("user_email"),
        "full_name": request.session.get("full_name")
    }
    return render(request, 'dashboard.html', context=context)


def Sidebar(request):
    """
    Renders the sidebar with active tab highlight.

    Args:
        request (HttpRequest): The HTTP request object. May contain `tab` GET param.

    Returns:
        HttpResponse: Rendered sidebar partial.
    """
    tab = request.GET.get("tab", "order")
    return render(request, "partials/sidebar.html", {"active_tab": tab})


def CreatePdf(order_id):
    """
    Utility function to prepare HTML strings for PDF and email rendering.

    Args:
        order_id (str): The ID of the Order object.

    Returns:
        Tuple[str, str, Order, Engineer, List[MaintenanceProtocol]]:
            - html_string for email body
            - html_string_pdf for the PDF
            - Order instance
            - Engineer instance
            - List of MaintenanceProtocol objects (excluding 'Sin revisar')
    """
    order = Order.objects.prefetch_related('maintenanceprotocol_set').get(id=order_id)
    engineer = Engineer.objects.get(id=order.engineer.id)
    protocols = order.maintenanceprotocol_set.all()
    filtered_protocols = [p for p in protocols if p.status != 'Sin revisar']

    html_string = render_to_string(
        'email/context.html',
        {
            'order': order,
            'protocols': filtered_protocols,
        }
    )

    html_string_pdf = render_to_string(
        'email/pdfDocument.html',
        {
            'order': order,
            'protocols': filtered_protocols,
            'engineer': engineer,
            'logo': OLYMPUS_LOGO,
        }
    )

    return html_string, html_string_pdf, order, engineer, protocols


def GenerateOrderPdf(request, order_id):
    """
    Generates and returns a PDF document for the specified order.

    Args:
        request (HttpRequest): The HTTP request object.
        order_id (str): The ID of the Order.

    Returns:
        HttpResponse: PDF file as an attachment.
    """
    html_string, html_string_pdf, order, engineer, protocols = CreatePdf(order_id)
    pdf = HTML(string=html_string_pdf).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orden_{order_id}.pdf"'
    return response


def SendPdfViaEmail(request, order_id):
    """
    Sends the generated PDF of the order to a fixed email address.

    Args:
        request (HttpRequest): The HTTP request object.
        order_id (str): The ID of the Order.

    Returns:
        JsonResponse: Status message indicating success.
    """
    html_string, html_string_pdf, order, engineer, protocols = CreatePdf(order_id)
    pdf_file = BytesIO()
    HTML(string=html_string_pdf).write_pdf(pdf_file)
    pdf_file.seek(0)

    email = EmailMultiAlternatives(
        subject=f'Orden de mantenimiento #{order_id}',
        from_email=engineer.email,
        to=["rmendoza.abd@hotmail.com"],
    )

    email.attach(f'orden_{order_id}.pdf', pdf_file.read(), 'application/pdf')
    email.attach_alternative(transform(html_string), "text/html")
    email.send()

    return JsonResponse({'status': 'success', 'message': 'Email sent successfully'}, status=200)
