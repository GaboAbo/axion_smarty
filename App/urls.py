"""
URL routing configuration for the core 'App'.

This module defines both frontend and API routes, as well as nested includes
for domain-specific apps such as Entity, Device, Order, and AuthUser.

Routes:
    - '' → Index view
    - 'home' → Home dashboard view
    - 'sidebar' → Sidebar UI component
    - 'auth/' → Microsoft OAuth2 authentication routes
    - 'api/entity/' → Entity-related API endpoints
    - 'api/device/' → Device-related API endpoints
    - 'api/order/' → Order-related API endpoints
    - 'api/user/' → Authenticated user and profile API endpoints
    - 'api/generatePdf/<order_id>' → Generate a PDF for a given order
    - 'api/sendPdf/<order_id>' → Send the generated PDF by email
"""

from django.urls import path, include

from .views import Index, HomeView, Sidebar, GenerateOrderPdf, SendPdfViaEmail

urlpatterns = [
    path('', Index, name='index'),  # Root view
    path('home', HomeView, name='home'),  # Dashboard view
    path('sidebar', Sidebar, name='sidebar'),  # Sidebar component

    # Microsoft OAuth2 authentication endpoints
    path('auth/', include("MicrosoftAuth.urls")),

    # API endpoints grouped by domain
    path('api/entity/', include("Entity.urls")),
    path('api/device/', include("Device.urls")),
    path('api/order/', include("Order.urls")),
    path('api/user/', include("AuthUser.urls")),

    # PDF generation and emailing endpoints
    path('api/generatePdf/<str:order_id>', GenerateOrderPdf, name='generatePdf'),
    path('api/sendPdf/<str:order_id>', SendPdfViaEmail, name='sendPdf'),
]
