from ..module import path
from .viewsGenders import GenderCreateView, GendersDestroyView, GenderListView, GenderUpdateView

urlpatterns = [
    path('', GenderListView.as_view()),
    path('update/<int:pk>', GenderUpdateView.as_view()),
    path('create/', GenderCreateView.as_view()),
    path('delete/<int:pk>', GendersDestroyView.as_view()),
]
