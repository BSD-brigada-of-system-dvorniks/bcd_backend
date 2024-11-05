from django.contrib import admin

from .models import Object


admin.site.unregister(Object)
