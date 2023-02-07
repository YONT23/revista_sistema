from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.autenticacion.api.views.auth.urls')),
    path('users/', include('apps.autenticacion.api.views.users.urls')),
    path('roles/', include('apps.autenticacion.api.views.roles.urls')),
    path('resources/', include('apps.autenticacion.api.views.resources.urls')),
    path('persons/', include('apps.autenticacion.api.views.persons.urls')),
    path('genders/', include('apps.autenticacion.api.views.genders.urls')),
    path('documents/', include('apps.autenticacion.api.views.documents.urls')),
    path('security/',include('apps.autenticacion.api.views.security.urls'))
]
