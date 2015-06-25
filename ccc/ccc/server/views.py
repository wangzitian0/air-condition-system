from django.shortcuts import render
from server.models import *
from server.forms import *
from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.contrib import messages
from django.conf import settings
from django.utils import timezone


def index(request):
    client = Client.objects.all().order_by('room_num')
    setting = Setting.objects.all()[0]
    time_now = timezone.localtime(timezone.now())
    for cl in client:
        if (time_now-cl.time_end).total_seconds()>setting.refresh*2:
            cl.connected='F'
        else:
            cl.connected='T'
        cl.save()
    return render_to_response('index.html',locals(),RequestContext(request))  


def clientboard(request,roomid):
    room = Client.objects.get(room_num = roomid)
    return render_to_response('client.html',locals(),RequestContext(request))  
# Create your views here.
def testboard(request,roomid):
    try:
        room = Client.objects.get(room_num = roomid)
        
    except:
        messages.error(request, 'Badrequest!')
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect('/')
    setting = Setting.objects.all()[0]
    #addnumber()
    if not room:
        return HttpResponseRedirect('/')
    if request.method=='POST':
        form = ClientForm(request.POST,instance = room)  
        #print form
        if form.is_valid():  
            form.save()  
            messages.success(request, 'Updated!')
        state = ClientstateForm(request.POST,instance = room)  
        if state.is_valid():  
            state.save()  
            messages.success(request, 'Updated!')
        sleep = ClientsleepForm(request.POST,instance = room)  
        if sleep.is_valid():  
            sleep.save()  
            messages.success(request, 'Updated!')
    form = ClientForm(instance = room) 
    state = ClientstateForm(instance = room)
    sleep = ClientsleepForm(instance = room)
    time_now = timezone.localtime(timezone.now())
    if (time_now-room.time_end).total_seconds()>setting.temp_refresh:
        thedelta = Price.objects.filter(speed=room.speed,mode=room.mode)[0].delta
        if room.temp_now<setting.normal:
            room.temp_now=min(room.temp_now+setting.tempback,setting.normal)
        else:
            room.temp_now=max(room.temp_now-setting.tempback,setting.normal)
        if room.sleep=='T' and getnumber()<setting.maxlinking:
            if (room.temp_now>room.temp_set+setting.tempsleep and room.mode=='C')or (room.temp_now+setting.tempsleep<room.temp_set and room.mode=='H'):
                room.sleep='F'
                addnumber()
        if room.sleep=='F':
            if room.mode=='H':
                room.temp_now=min(room.temp_now+thedelta,room.temp_set)
            else:
                room.temp_now=max(room.temp_now+thedelta,room.temp_set)
                print "haha",thedelta
            if room.temp_now==room.temp_set:
                Cost.addCostRecord(room)
                room.sleep='T'
                delnumber()
        room.save()
        Client.refreshRecord(room)
    msg=messages.get_messages(request)
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
    thedelta = Price.objects.filter(speed=room.speed,mode=room.mode)[0].delta
    if not room:
        pass
    else:
        Client.refreshRecord(room)
    if request.method=='POST':
        form = ClientForm(request.POST,instance = room)  
        print form
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











def fclient(request):

    if request.method=='POST':
        
        roomid = request.POST['roomid']
        print 'roomid',roomid
        client_power = request.POST['power']
        client_mode = request.POST['mode']
        client_temp = request.POST['temp']
        client_aim_temp = request.POST['aim_temp']
        client_state = request.POST['room_state']
        client_start = request.POST['start']
        room = Client.objects.get(room_num = roomid)
        print 'room',room
        if not room:
            pass
        else:
            Client.refreshRecord(room)
        form = ClientallForm(instance = room)  
        if client_power==0.2:
            form.speed='1'
        elif client_power == 0.4:
            form.speed='2'
        else:
            form.speed='3'

        if client_state == 'on' and client_mode == 'cold' and client_temp <= client_aim_temp:
            form.sleep='T'
        elif client_state == 'on' and client_mode == 'warm' and cient_temp >= client_aim_temp:
            form.sleep = 'T'
        else :
            form.sleep='F'
        form.temp_now=client_temp
        form.temp_set=client_aim_temp
        
        if client_mode == 'cold':
            form.mode = 'C'
        elif client_mode == 'warm':
            form.mode = 'H' 



        if form.is_valid():  
            form.save()  
            if form.has_changed():
                Cost.addCostRecord(room)
    from django.http import HttpResponse
    return HttpResponse('yes')
    #form = ClientallForm(instance = room) 
    #return render_to_response('board.html',locals(),RequestContext(request))  

