from django.db import models
import datetime
# Create your models here.
class Const():
    BOOL_CHOICES = (
        ('T','True'),
        ('F','False'),
    )

    MODE_CHOICES = (
        ('U','UNSET'),
        ('C','COLD'),
        ('H','HOT'),
    )
    SPEED_CHOICES = (
        ('0','UNSET'),
        ('1','LOW'),
        ('2','MIDDLE'),
        ('3','HIGH'),
    )
class Price(models.Model):
    speed = models.CharField(max_length=1,choices=Const.SPEED_CHOICES,default='0')
    mode = models.CharField(max_length=1,choices=Const.MODE_CHOICES,default='U')
    price = models.FloatField()
    delta = models.FloatField(default=0)
class Setting(models.Model):
    normal = models.FloatField(default=18)
    refresh = models.IntegerField(default=5)
    temp_refresh = models.IntegerField(default=5)
    maxlinking = models.IntegerField(default=3)
    tempback = models.FloatField(default=0.2)
    tempsleep = models.FloatField(default=1.5)
class Clientnumber(models.Model):
    number = models.IntegerField(default=0) 

def addnumber():
    clientnumber = Clientnumber.objects.all()[0]
    clientnumber.number += 1
    clientnumber.save() 
def delnumber():
    clientnumber = Clientnumber.objects.all()[0]
    clientnumber.number -= 1
    clientnumber.save() 
def getnumber():
    clientnumber = Clientnumber.objects.all()[0]
    return clientnumber.number

class Client(models.Model):
    room_num = models.IntegerField(unique=True)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    temp_now = models.FloatField()
    temp_set = models.FloatField()
    speed = models.CharField(max_length=1,choices=Const.SPEED_CHOICES,default='0')
    mode = models.CharField(max_length=1,choices=Const.MODE_CHOICES,default='U')
    connected = models.CharField(max_length=1,choices=Const.BOOL_CHOICES,default='F')
    sleep = models.CharField(max_length=1,choices=Const.BOOL_CHOICES,default='F')

    @classmethod
    def refreshRecord(cls,room):
        if room.sleep=='T':
            room.time_start = datetime.datetime.now()
        room.time_end = datetime.datetime.now()
        room.save()


class Cost(models.Model):
    room_num = models.IntegerField()
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    speed = models.CharField(max_length=1,choices=Const.SPEED_CHOICES,default='0')
    mode = models.CharField(max_length=1,choices=Const.MODE_CHOICES,default='U')

    @classmethod
    def addCostRecord(cls,room):
        if room.sleep=='F':
            costrecord = Cost()
            costrecord.room_num = room.room_num
            costrecord.time_start = room.time_start
            costrecord.time_end = room.time_end
            costrecord.speed = room.speed
            costrecord.mode = room.mode
            costrecord.save()
    @classmethod
    def getTheDayCost(cls,room_num):
        qs = Cost.objects.filter(room_num=room_num)
        dic = []
        timeNow = datetime.datetime.now()
        aDay = datetime.timedelta(days=1)
        for i in range(0,30):
            timeQuery = timeNow - aDay * i
            ds = qs.filter(time_end__year=timeQuery.year,time_end__month=timeQuery.month,time_end__day=timeQuery.day)
            dateS=timeQuery.strftime('%Y-%m-%d')
            timeS =  datetime.timedelta(0) 
            priceS = 0
            for it in ds:
                timeS += it.time_end-it.time_start
                price = Price.objects.filter(speed=it.speed,mode=it.mode)[0].price
                pT = (it.time_end-it.time_start).total_seconds()/60
                if(pT<0):pT = 0
                priceS += pT*price
            dic.append((dateS,timeS,priceS))
        return dic
    @classmethod
    def getTheMonthCost(cls,room_num):
        pass
