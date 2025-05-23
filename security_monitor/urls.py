from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.monitoring_page, name='monitoring'),
    path('add/', views.add_domain, name='add_domain'),
    path('list/', views.domain_list, name='domain_list'),
]
