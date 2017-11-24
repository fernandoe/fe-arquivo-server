from django.conf.urls import url
from django.contrib import admin

from arquivo.views import ArquivoUploadAPIView, ArquivoAPIView, ArquivoDownloadAPIView
from healthcheck.views import HealthCkeckAPIView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^healthcheck', HealthCkeckAPIView.as_view()),
    url(r'^api/v1/arquivo$', ArquivoUploadAPIView.as_view()),
    url(r'^api/v1/arquivo/(?P<uuid>.+)/download$', ArquivoDownloadAPIView.as_view(), name='arquivo_download'),
    url(r'^api/v1/arquivo/(?P<uuid>.+)$', ArquivoAPIView.as_view(), name='arquivo'),
]
