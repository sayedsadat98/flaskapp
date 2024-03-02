from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", BasicEmailView.as_view(), name='my_form_view')

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
