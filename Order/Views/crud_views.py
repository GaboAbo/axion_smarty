from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from Order.models import Order, MaintenanceProtocol

from Entity.models import Contract

from Device.models import Device

from Order.forms import OrderForm


# Create your views here.
def GetAllOrders(request):
    return render(request, "order/list.html", {'active_tab': 'order'})


def GetOrderByID(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "order/orderView.html", {"order": order})


def CreateOrder(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "order/list.html", {})
    form = OrderForm()
    return render(request, "order/create.html", {"form": form})


def UpdateOrder(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return render(request, "order/list.html", {})
        
    form = OrderForm(instance=order)
    return render(request, "order/update.html", {"form": form, "order_pk": order_pk})


def DeleteOrder(request, order_pk):
    Order.objects.get(pk=order_pk).delete()
    return render(request, "order/list.html", {})


def ContractByClient(request):
    client = request.GET.get("client")
    contracts = Contract.objects.filter(entity__pk=client)
    return render(request, "order/partial/contractSelector.html", {"contracts": contracts})


def DevicesByClient(request):
    client = request.GET.get("client")
    contract = request.GET.get("contract")
    devices = Device.objects.filter(client__pk=client)
    if contract:
        devices = devices.filter(contract__pk=contract)
    return render(request, "order/partial/deviceSelector.html", {"devices": devices})


def ProtocolsByOrder(request, order_pk):
    protocols = MaintenanceProtocol.objects.filter(order__pk=order_pk).defer("fields")
    return render(request, "order/partial/deviceList.html", {"protocols": protocols})


def FilterOrder(request):
    orders = Order.objects.all()
    id = request.GET.get("id")
    client = request.GET.get("client")
    engineer = request.GET.get("engineer")
    exec_date = request.GET.get("exec_date")
    model = request.GET.get("model")
    serial = request.GET.get("serial")
    status = request.GET.get("status")
    if id:
        orders = orders.filter(pk=id)
    if client:
        orders = orders.filter(client__name__icontains=client)
    if engineer:
        orders = orders.filter(engineer=engineer)
    if status:
        orders = orders.filter(status=status)
    if exec_date:
        orders = orders.filter(created_at=exec_date)
    if model:
        orders = orders.filter(device__device_model__part_number__icontains=model)
    if serial:
        orders = orders.filter(device__serial_number=model)
    return render(request, "order/partial/table.html", {"orders": orders})
