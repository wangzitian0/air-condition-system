from django.shortcuts import render
from server.models import *
from server.forms import *
from django.shortcuts import render, render_to_response, RequestContext, redirect


def index(request):
    client = Client.objects.all().order_by('room_num')
    return render_to_response('index.html',locals(),RequestContext(request))  


def clientboard(request,roomid):
    room = Client.objects.get(room_num = roomid)
    return render_to_response('client.html',locals(),RequestContext(request))  
# Create your views here.
def testboard(request,roomid):
    room = Client.objects.get(room_num = roomid)
    if not room:
        pass
    else:
        Client.refreshRecord(room)
    if request.method=='POST':
        form = ClientForm(request.POST,instance = room)  
        if form.is_valid():  
            form.save()  
        state = ClientstateForm(request.POST,instance = room)  
        if state.is_valid():  
            state.save()  
        sleep = ClientsleepForm(request.POST,instance = room)  
        if sleep.has_changed():
            Cost.addCostRecord(room)
        if sleep.is_valid():  
            sleep.save()  
    form = ClientForm(instance = room) 
    state = ClientstateForm(instance = room)
    sleep = ClientsleepForm(instance = room)
    return render_to_response('testboard.html',locals(),RequestContext(request))  

def testdaycost(request,roomid):
    costlist = Cost.getTheDayCost(roomid)
    room = Client.objects.get(room_num = roomid)
    period = 'Daily'
    return render_to_response('cost.html',locals(),RequestContext(request))  

def testmonthcost(request,roomid):
    pass

def postboard(request,roomid):
    room = Client.objects.get(room_num = roomid)
    if not room:
        pass
    else:
        Client.refreshRecord(room)
    if request.method=='POST':
        form = ClientForm(request.POST,instance = room)  
        if form.is_valid():  
            form.save()  
        state = ClientstateForm(request.POST,instance = room)  
        if state.is_valid():  
            state.save()  
        sleep = ClientsleepForm(request.POST,instance = room)  
        if sleep.has_changed():
            Cost.addCostRecord(room)
        if sleep.is_valid():  
            sleep.save()  
    form = ClientForm(instance = room) 
    state = ClientstateForm(instance = room)
    sleep = ClientsleepForm(instance = room)
    return render_to_response('testboard.html',locals(),RequestContext(request))  

