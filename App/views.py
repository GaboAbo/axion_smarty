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


# Create your views here.
def Index(request):
    email = request.session.get("user_email")
    name = request.session.get("full_name")
    if name and email:
        return redirect("home")
    return render(request, 'index.html')


def HomeView(request):
    context = {
        "user_email": request.session.get("user_email"),
        "full_name": request.session.get("full_name")
    }
    return render(request, 'dashboard.html', context=context)


def Sidebar(request):
    tab = request.GET.get("tab", "order")
    return render(request, "partials/sidebar.html", {"active_tab": tab})


def CreatePdf(order_id):
    order = (Order.objects.prefetch_related('maintenanceprotocol_set').get(id=order_id))
    engineer = Engineer.objects.get(id=order.engineer.id)
    protocols = order.maintenanceprotocol_set.all()
    filteret_protocols = [protocol for protocol in protocols if protocol.status != 'Sin revisar']

    html_string = render_to_string(
        'email/context.html',
        {
            'order': order,
            'protocols': filteret_protocols,
        }
    )

    html_string_pdf = render_to_string(
        'email/pdfDocument.html',
        {
            'order': order,
            'protocols': filteret_protocols,
            'engineer': engineer,
            'logo': OLYMPUS_LOGO,
        }
    )

    return html_string, html_string_pdf, order, engineer, protocols


def GenerateOrderPdf(request, order_id):
    html_string, html_string_pdf, order, engineer, protocols = CreatePdf(order_id)
    
    pdf = HTML(string=html_string_pdf).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orden_{order_id}.pdf"'

    return response

    
def SendPdfViaEmail(request, order_id):
    html_string, html_string_pdf, order, engineer, protocols = CreatePdf(order_id)
    pdf_file = BytesIO()
    HTML(string=html_string_pdf).write_pdf(pdf_file)
    pdf_file.seek(0)
    
    email = EmailMultiAlternatives(
        subject=f'Order de mantenimiento #{order_id}',
        from_email=engineer.email,
        to=["rmendoza.abd@hotmail.com"],
    )

    email.attach(f'orden_{order_id}.pdf', pdf_file.read(), 'application/pdf')
    email.attach_alternative(transform(html_string), "text/html")
    email.send()

    return JsonResponse({'status': 'success', 'message': 'Email sent successfully'}, status=200)