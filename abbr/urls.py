from django.conf.urls import url, include
from django.contrib import admin

admin.site.site_header = 'ABBR'
admin.site.site_title = 'ABBR'

urlpatterns = [
    url(r'', include('abbr.doacoes.urls', namespace='doacoes')),
    url(r'^admin/', admin.site.urls),
]
