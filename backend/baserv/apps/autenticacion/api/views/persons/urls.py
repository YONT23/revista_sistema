from ..module import path
from .viewsPerson import PersonCreateView, PersonView, PersonUpdateView, CreateAPIView

urlpatterns = [
    path('', PersonView.as_view()),
    path('update/<int:pk>/', PersonUpdateView.as_view()),
    path('create/', PersonCreateView.as_view())
]
