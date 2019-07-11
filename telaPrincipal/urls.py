from . import views
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

app_name = 'telaPrincipal'

urlpatterns = [
    url(r'^$', view=views.index, name='index'),

    url('accounts/login/', auth_views.LoginView.as_view(), name='loginForm'),
    url('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^ajax/carregarmo/', views.carregarMO, name='ajaxCarregarMO'),
    url(r'^ajax/carregariteminspecao/', views.carregarItemInspecao, name='ajaxCarregarItemInspecao'),
    url(r'^ajax/registrarinspecao/', views.registrarInspecao, name='ajaxRegistrarInspecao'),
    url(r'^pdf/PDF_IPXX_XXX_19/$', views.PDF_IPXX_XXX_19, name='PDF_IPXX_XXX_19'),
]
