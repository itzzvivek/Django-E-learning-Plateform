from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('subjects/',views.SubjectListView.as_view(),name='subject_list'),
    path('subjects/<pk>/',views.SubjectDetailsViews.as_view(),name='subject_detail')
]
