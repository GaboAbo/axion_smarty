from django.shortcuts import render

from Device.models import Device


# Create your views here.
def GetAllDevices(request):
    return render(request, "device/list.html", {'active_tab': 'device'})


def FilterDevice(request):
    devices = Device.objects.all()
    client = request.GET.get("client")
    contract = request.GET.get("contract")
    model = request.GET.get("model")
    serial = request.GET.get("serial")
    if client:
        devices = devices.filter(client__name__icontains=client)
    if contract:
        devices = devices.filter(contract__number=contract)
    if model:
        devices = devices.filter(device_model__part_number__icontains=model)
    if serial:
        devices = devices.filter(serial_number=model)
    return render(request, "device/partial/table.html", {"devices": devices})
