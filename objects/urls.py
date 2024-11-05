from django.urls import path

from .views import ObjectListView, ObjectCreateView, \
                   ObjectDetailView, ObjectUpdateView, ObjectDeleteView


appname = 'objects'
urlpatterns = [
    path('',                ObjectListView.as_view(),   name = 'object-list'),
    path('create/',          ObjectCreateView.as_view(), name = 'object-create'),
    path('<str:id>/',        ObjectDetailView.as_view(), name = 'object-detail'),
    path('<str:id>/update/', ObjectUpdateView.as_view(), name = 'object-update'),
    path('<str:id>/delete/', ObjectDeleteView.as_view(), name = 'object-delete'),
]
