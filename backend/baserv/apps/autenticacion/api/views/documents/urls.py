from ..module import path
from .viewsDocuments import DocumentListView, DocumentDestroyView, DocumentUpdateView, DocumentCreateView

urlpatterns = [
    path('', DocumentListView.as_view()),
    path('update/<int:pk>', DocumentUpdateView.as_view()),
    path('create/', DocumentCreateView.as_view()),
    path('delete/<int:pk>', DocumentDestroyView.as_view()),
]
