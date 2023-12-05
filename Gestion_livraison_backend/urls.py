from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    EtatsColisView, ExpediteurViewSet, ColisViewSet, DepotViewSet, LivreurViewSet,
    EtatViewSet, EtatColisViewSet, ReclamationViewSet, RecetteExpediteurViewSet, colis_par_expediteur_et_etat, registration_view,TestView
    
)

router = DefaultRouter()
router.register('expediteurs', ExpediteurViewSet)
router.register('colis', ColisViewSet)
router.register('depots', DepotViewSet)
router.register('livreurs', LivreurViewSet)
router.register('etats', EtatViewSet)
router.register('etatcolis', EtatColisViewSet)
router.register('reclamations', ReclamationViewSet)
router.register('recettesexpediteurs', RecetteExpediteurViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/colis/list_colis_expediteur_by_etat/<int:code_expediteur>/<int:code_etat>/', colis_par_expediteur_et_etat, name='ma_vue'),
    path('api/etats_colis/<str:cc>/', EtatsColisView.as_view(), name='etats_colis'),
    path('api/test/', TestView.as_view(), name='test_view'),




    path('register', registration_view, name="register"),
	path('login', obtain_auth_token, name="login"),
]
