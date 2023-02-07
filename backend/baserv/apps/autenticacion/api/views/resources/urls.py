from ..module import path
from .viewsResources import  ResourcesListView, ResourcesDestroyView, ResourcesUpdateView

urlpatterns = [
    path('roles/', ResourcesListView.as_view()),
    path('update/<int:pk>', ResourcesUpdateView.as_view()),
    path('delete/<int:pk>', ResourcesDestroyView.as_view()),
]
