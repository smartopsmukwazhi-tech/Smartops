from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkin/', views.checkin_analyser, name='checkin_analyser'),
    path('ramp/', views.ramp_analyser, name='ramp_analyser'),
    path('sla/', views.checkin_sla, name='checkin_sla'),
    path('api/checkin-sla/', views.checkin_sla_api, name='checkin_sla_api'),
]
