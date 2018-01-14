from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^auth/$', views.LoginView.as_view(), name="login"),
    url(r'^$', login_required(TemplateView.as_view(template_name="components/index.html"))),
    url(r'^blank/$', login_required(TemplateView.as_view(template_name="components/blank.html"))),
    url(r'^buttons/$', login_required(TemplateView.as_view(template_name="components/buttons.html"))),
    url(r'^flot/$', login_required(TemplateView.as_view(template_name="components/flot.html"))),
    url(r'^forms/$', login_required(TemplateView.as_view(template_name="components/forms.html"))),
    url(r'^grid/$', login_required(TemplateView.as_view(template_name="components/grid.html"))),
    url(r'^icons/$', login_required(TemplateView.as_view(template_name="components/icons.html"))),
    url(r'^morris/$', login_required(TemplateView.as_view(template_name="components/morris.html"))),
    url(r'^notifications/$', login_required(TemplateView.as_view(template_name="components/notifications.html"))),
    url(r'^panels/$', login_required(TemplateView.as_view(template_name="components/panels.html"))),
    url(r'^tables/$', login_required(TemplateView.as_view(template_name="components/tables.html"))),
    url(r'^typography/$', login_required(TemplateView.as_view(template_name="components/typography.html"))),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
]
