from django.urls import path
from .viewsRoles import RolesListView, RolesCreateView, RoleUpdateView, RolesDestroyView

urlpatterns = [
    path('', RolesListView.as_view()),
    path('create/', RolesCreateView.as_view()),
    path('update/<int:pk>', RoleUpdateView.as_view()),
    path('delete/<int:pk>', RolesDestroyView.as_view())
]
