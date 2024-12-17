from django.urls import path
from .views import input_view

urlpatterns = [
    path('', input_view, name='input_view'),
]