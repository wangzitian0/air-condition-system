from django import forms
from server.models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('room_num','mode','temp_now' ,'temp_set', 'speed')
        #widgets = {
        #    'room_num': forms.HiddenInput(attrs={'readonly': True}),
        #    #'temp_now': forms.NumberInput(attrs={'readonly': True}),
        #    'mode': forms.Select(attrs={'disabled': True}),
        #}


class ClientallForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('room_num','temp_set','temp_now' , 'speed','mode','sleep','connected')

class ClientstateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('connected',)

class ClientsleepForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('sleep',)

