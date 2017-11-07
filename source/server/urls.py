from django.conf.urls import url
from django.contrib import admin

from arquivo.views import ArquivoUploadAPIView
from healthcheck.views import HealthCkeckAPIView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^healthcheck', HealthCkeckAPIView.as_view()),
    url(r'^api/v1/arquivo', ArquivoUploadAPIView.as_view())
]
