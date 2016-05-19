from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'', include('abbr.doacoes.urls', namespace='doacoes')),
    url(r'^admin/', admin.site.urls),
]
