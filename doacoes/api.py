from rest_framework import routers

from .doacoes import views as doacao_views

router = routers.DefaultRouter()
router.register(r'doacoes', doacao_views.DoacaoViewSet, base_name='doacoes')
