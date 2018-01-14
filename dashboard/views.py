from django.views.generic import TemplateView
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.contrib.auth.decorators import login_required
from dashboard.models import *

class IndexView(TemplateView):
    template_name = "components/index.html"
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'title': "Dashboard"})
        return context

class BlankView(TemplateView):
    template_name = "components/blank.html"
    def get_context_data(self, **kwargs):
        context = super(BlankView, self).get_context_data(**kwargs)
        context.update({'title': "Blank Page"})
        return context

class ButtonsView(TemplateView):
    template_name = "components/buttons.html"
    def get_context_data(self, **kwargs):
        context = super(ButtonsView, self).get_context_data(**kwargs)
        context.update({'title': "Buttons"})
        return context

class FlotView(TemplateView):
    template_name = "components/flot.html"
    def get_context_data(self, **kwargs):
        context = super(FlotView, self).get_context_data(**kwargs)
        context.update({'title': "Flot Charts"})
        return context

class FormsView(TemplateView):
    template_name = "components/forms.html"
    def get_context_data(self, **kwargs):
        context = super(FormsView, self).get_context_data(**kwargs)
        context.update({'title': "Forms"})
        return context

class GridView(TemplateView):
    template_name = "components/grid.html"
    def get_context_data(self, **kwargs):
        context = super(GridView, self).get_context_data(**kwargs)
        context.update({'title': "Grid"})
        return context

class IconsView(TemplateView):
    template_name = "components/icons.html"
    def get_context_data(self, **kwargs):
        context = super(IconsView, self).get_context_data(**kwargs)
        context.update({'title': "Icons"})
        return context


class LoginView(FormView):
    template_name = "components/login.html"
    success_url = "/"
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)
    def get_success_url(self):

        redirect_to = self.request.POST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context.update({'title': "Log In"})
        return context

                                                                    

class MorrisView(TemplateView):
    template_name = "components/morris.html"
    def get_context_data(self, **kwargs):
        context = super(MorrisView, self).get_context_data(**kwargs)
        context.update({'title': "Morris Charts"})
        return context

class NotificationsView(TemplateView):
    template_name = "components/notifications.html"
    def get_context_data(self, **kwargs):
        context = super(NotificationsView, self).get_context_data(**kwargs)
        context.update({'title': "Notifications"})
        return context

class PanelsView(TemplateView):
    template_name = "components/panels-wells.html"
    def get_context_data(self, **kwargs):
        context = super(PanelsView, self).get_context_data(**kwargs)
        context.update({'title': "Panels and Wells"})
        return context

class TablesView(TemplateView):
    template_name = "components/tables.html"
    def get_context_data(self, **kwargs):
        context = super(TablesView, self).get_context_data(**kwargs)
        context.update({'title': "Tables"})
        return context

class TypographyView(TemplateView):
    template_name = "components/typography.html"
    def get_context_data(self, **kwargs):
        context = super(TypographyView, self).get_context_data(**kwargs)
        context.update({'title': "Typography"})
        return context

class LogoutView(RedirectView):
    url = '/auth/'
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

class ServerView(TemplateView):
	template_name = "components/server_tables.html"
	def get_context_data(self, **kwargs):
		context = super(ServerView, self).get_context_data(**kwargs)
		context.update({'title': "Server Information"})
		context['server_fields'] = [ f.name for f in Server._meta.get_fields(include_hidden=False) ]
		services_in_server = []
		for i in Server.objects.all():
			services_in_server.append(Service.objects.filter(server_id=i.id))
		accounts_in_server = []
		for i in Server.objects.all():
			accounts_in_server.append(Server_account.objects.filter(server_id=i.id))
		interfaces_in_server = []
		for i in Server.objects.all():
			interfaces_in_server.append(Interface.objects.filter(server_id=i.id))
		context['servers'] = zip(Server.objects.all(), services_in_server, accounts_in_server, interfaces_in_server)
		return context


