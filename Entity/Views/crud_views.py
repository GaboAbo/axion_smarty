from django.shortcuts import render

from Entity.models import Entity, Contract

from App.constants import BRIDGE


# Create your views here.
def GetAllClients(request):
    return render(request, "entity/client/list.html", {"bridge": BRIDGE})


def GetAllContracts(request):
    return render(request, "entity/contract/list.html", {"bridge": BRIDGE})
