from django.contrib import admin
from .models import Router, ApplicationRouter, AddedRouter

# Register your models here.

admin.site.register(Router)
admin.site.register(ApplicationRouter)
admin.site.register(AddedRouter)