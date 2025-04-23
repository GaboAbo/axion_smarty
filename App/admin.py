from django.contrib import admin

from oauth2_provider.models import Application

from Entity.models import Entity, Contract, Area

from AuthUser.models import Engineer, Client

from Device.models import DeviceModel, Device

from Order.models import Order, MaintenanceProtocol

# Register your models here.
admin.site.register(Entity)
admin.site.register(Contract)
admin.site.register(Area)
admin.site.register(Engineer)
admin.site.register(Client)
admin.site.register(DeviceModel)
admin.site.register(Device)
admin.site.register(Order)
admin.site.register(MaintenanceProtocol)
