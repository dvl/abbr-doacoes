from django.conf.urls import url, include
from django.contrib import admin

from . import api

urlpatterns = [
    url(r'', include('doacoes.doacoes.urls', namespace='doacoes')),
    url(r'^api/', include(api.router.urls)),
    url(r'^admin/', admin.site.urls),
]
