from django.contrib import admin
from apps.autenticacion.models import *
# Register your models here.


admin.site.register(Document_types)
admin.site.register(Genders)
admin.site.register(Users)
admin.site.register(User_roles)
admin.site.register(Persons)
admin.site.register(Resources)
admin.site.register(Resources_roles)
admin.site.register(Roles)