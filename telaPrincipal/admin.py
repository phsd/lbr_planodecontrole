from django.contrib import admin
from .models import headerPlanoControle, itemInspecaoPC, inspecaoPlanoControle

# Register your models here.

admin.site.register(headerPlanoControle)
admin.site.register(itemInspecaoPC)
admin.site.register(inspecaoPlanoControle)
