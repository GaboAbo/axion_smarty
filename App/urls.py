from django.urls import path, include

from .views import Index, HomeView, Sidebar, GenerateOrderPdf, SendPdfViaEmail


urlpatterns = [
    path('', Index, name='index'),
    path('home', HomeView, name='home'),
    path('sidebar', Sidebar, name='sidebar'),
    
    path('auth/', include("MicrosoftAuth.urls")),
    path('api/entity/', include("Entity.urls")),
    path('api/device/', include("Device.urls")),
    path('api/order/', include("Order.urls")),
    path('api/user/', include("AuthUser.urls")),
    path('api/generatePdf/<str:order_id>', GenerateOrderPdf, name='generatePdf'),
    path('api/sendPdf/<str:order_id>', SendPdfViaEmail, name='sendPdf'),
]
