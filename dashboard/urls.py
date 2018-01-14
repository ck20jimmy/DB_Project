from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url(r'^auth/$', views.LoginView.as_view(), name="login"),
    url(r'^service/$', login_required(views.ServiceView.as_view(template_name="components/service_tables.html")), name="service"), 
    url(r'^switch/$', login_required(views.SwitchView.as_view(template_name="components/switch_tables.html")), name="switch"),
    url(r'^interface/$', login_required(views.InterfaceView.as_view(template_name="components/interface_tables.html")), name="interface"),
    url(r'^$', login_required(views.IndexView.as_view(template_name="components/index.html")), name="index"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
]

