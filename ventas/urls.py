from django.urls import path
from . import views

urlpatterns = [
    path('api/ventas/', views.ventas_api_list, name='ventas_api_list'),
]
