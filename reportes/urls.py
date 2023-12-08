from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import dashboard_view

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
]

urlpatterns = format_suffix_patterns(urlpatterns)