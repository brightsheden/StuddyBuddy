from django.contrib import admin
from django.db.models.base import ModelStateFieldsCacheDescriptor
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)



