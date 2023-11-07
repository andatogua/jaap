from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from parameters.views import ParameterList

urlpatterns = [
    path('parametros/', ParameterList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)