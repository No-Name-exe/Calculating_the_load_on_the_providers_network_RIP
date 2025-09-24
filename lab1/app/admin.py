from django.contrib import admin
from .models import Router, Application, AddedRouter

# Register your models here.

admin.site.register(Router)
admin.site.register(Application)
admin.site.register(AddedRouter)