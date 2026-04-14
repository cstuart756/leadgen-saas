from django.urls import path
from . import views

urlpatterns = [
    path('u/<str:username>/', views.lead_capture, name='lead_capture'),
    path('dashboard/leads/', views.lead_list, name='lead_list'),
]