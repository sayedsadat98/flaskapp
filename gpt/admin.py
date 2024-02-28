from django.contrib import admin
from .models import UserPlan,UserServiceLimit,Service,ApiRequest,Emails
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


class CustomAdminSite(AdminSite):
    site_header = _("308GPT Admin DashBoard")
    site_title = _("308GPT Admin DashBoard")
    index_title = _("Welcome to 308GPT Admin DashBoard")

custom_admin_site = CustomAdminSite(name="308GPT Admin DashBoard")
custom_admin_site._registry = admin.site._registry

# Register your models here.

admin.site.register(UserPlan)
admin.site.register(UserServiceLimit)
admin.site.register(Service)
admin.site.register(ApiRequest)
admin.site.register(Emails)