from django.urls import path
from . import views

urlpatterns = [
    path('', views.evidence_list, name='evidence_list'),
    path('upload/', views.evidence_upload, name='evidence_upload'),
    path('<int:pk>/', views.evidence_detail, name='evidence_detail'),
] 