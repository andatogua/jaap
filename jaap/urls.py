"""jaap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import CustomLoginView,CustomLogoutView, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/',include('autenticacion.urls')),
    path('api/',include('registro.urls')),
    path('api/', include('parameters.urls')),
    path('pagos/', include('pagos.urls')),
    path('reportes/', include('reportes.urls')),
    path('asignados/', include('asignados.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

admin.site.site_url = "/reportes/dashboard"