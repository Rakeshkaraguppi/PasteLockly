from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('snippet/<int:snippet_id>/', views.view_snippet, name='view_snippet'),
]
