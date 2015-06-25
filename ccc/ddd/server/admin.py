from django.contrib import admin
from server.models import * 

#admin.site.register(cost)
#admin.site.register(client)

def mark_allcold(modeladmin, request, queryset):
    queryset.update(mode='C')
mark_allcold.short_description = "Mark mode all as COLD"

def mark_allhot(modeladmin, request, queryset):
    queryset.update(mode='H')
mark_allhot.short_description = "Mark mode all as HOT"

def mark_alllow(modeladmin, request, queryset):
    queryset.update(speed='1')
mark_alllow.short_description = "Mark speed all as low"

def mark_allmiddle(modeladmin, request, queryset):
    queryset.update(speed='2')
mark_allmiddle.short_description = "Mark speed all as middle"

def mark_allhigh(modeladmin, request, queryset):
    queryset.update(speed='3')
mark_allhigh.short_description = "Mark speed all as high"


class ClientAdmin(admin.ModelAdmin):
    fields = ('room_num','time_start','time_end','temp_set','temp_now' , 'speed','mode','sleep','connected')
    list_display = ('room_num','time_start','time_end','temp_set','temp_now' , 'speed','mode','sleep','connected')
    ordering = ['room_num'] 
    actions = [mark_allhot,mark_allcold,mark_alllow,mark_allmiddle,mark_allhigh,]

class CostAdmin(admin.ModelAdmin):
    fields = ('room_num','time_start','time_end', 'speed','mode')
    list_display = ('room_num','time_start','time_end', 'speed','mode')

class PriceAdmin(admin.ModelAdmin):
    fields = ('price', 'speed','mode')
    list_display = ('price', 'speed','mode')

admin.site.register(Client, ClientAdmin)
admin.site.register(Cost, CostAdmin)
admin.site.register(Price, PriceAdmin)
# Register your models here.
