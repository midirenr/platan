from django.contrib import admin
from .models import *


admin.site.register(Devices)
admin.site.register(SerialNumPCB)
admin.site.register(SerialNumBoard)
admin.site.register(SerialNumRouter)
admin.site.register(SerialNumBP)
admin.site.register(SerialNumCase)
admin.site.register(SerialNumPackage)
admin.site.register(SerialNumPKI)
admin.site.register(Macs)
admin.site.register(DeviceType)
admin.site.register(ModificationType)
admin.site.register(DetailType)
admin.site.register(PlaceOfProduction)
admin.site.register(Statistic)
admin.site.register(History)
admin.site.register(Repair)