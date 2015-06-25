from django.forms import ModelForm
from server.models import Client

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ('room_num','temp_set','temp_now' , 'speed','mode')


class ClientallForm(ModelForm):
    class Meta:
        model = Client
        fields = ('room_num','temp_set','temp_now' , 'speed','mode','sleep','connected')

class ClientstateForm(ModelForm):
    class Meta:
        model = Client
        fields = ('connected',)

class ClientsleepForm(ModelForm):
    class Meta:
        model = Client
        fields = ('sleep',)

