from django.urls import path

from .views import ObjectListView, ObjectCreateView, \
                   ObjectDetailView, ObjectUpdateView, ObjectDeleteView


appname = 'articles'
urlpatterns = [
    path('objects/',                 ObjectListView.as_view(),   name = 'list'),
    path('objects/create/',          ObjectCreateView.as_view(), name = 'create'),
    path('objects/<str:id>/',        ObjectDetailView.as_view(), name = 'detail'),
    path('objects/<str:id>/update/', ObjectUpdateView.as_view(), name = 'update'),
    path('objects/<str:id>/delete/', ObjectDeleteView.as_view(), name = 'delete'),
]
