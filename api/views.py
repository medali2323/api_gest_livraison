from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Subquery, OuterRef
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Expediteur, Colis, Depot, Livreur, Etat, EtatColis, Reclamation, RecetteExpediteur
from .serializers import (
    ExpediteurSerializer, ColisSerializer, DepotSerializer, LivreurSerializer,
    EtatSerializer, EtatColisSerializer, ReclamationSerializer, RecetteExpediteurSerializer, RegistrationSerializer
)
from django.db.models import F
from django.http import HttpResponse
from django.views import View
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

class ExpediteurViewSet(viewsets.ModelViewSet):
    queryset = Expediteur.objects.all()
    serializer_class = ExpediteurSerializer

class ColisViewSet(viewsets.ModelViewSet):
    queryset = Colis.objects.all()
    serializer_class = ColisSerializer

   
class DepotViewSet(viewsets.ModelViewSet):
    queryset = Depot.objects.all()
    serializer_class = DepotSerializer

class LivreurViewSet(viewsets.ModelViewSet):
    queryset = Livreur.objects.all()
    serializer_class = LivreurSerializer

class EtatViewSet(viewsets.ModelViewSet):
    queryset = Etat.objects.all()
    serializer_class = EtatSerializer

class EtatColisViewSet(viewsets.ModelViewSet):
    queryset = EtatColis.objects.all()
    serializer_class = EtatColisSerializer

class ReclamationViewSet(viewsets.ModelViewSet):
    queryset = Reclamation.objects.all()
    serializer_class = ReclamationSerializer

class RecetteExpediteurViewSet(viewsets.ModelViewSet):
    queryset = RecetteExpediteur.objects.all()
    serializer_class = RecetteExpediteurSerializer
@api_view(['POST', ])
def registration_view(request):

	if request.method == 'POST':
        
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			token = Token.objects.get(user=account).key
			data['token'] = token
           
		else:
			data = serializer.errors
		return Response(data)
class EtatsColisView(APIView):
    def get(self, request, cc, format=None):
        etats_colis = EtatColis.objects.filter(code_colis__code_colis=cc).order_by('date')
        serializer = EtatColisSerializer(etats_colis, many=True)

        # Si les données sont déjà sérialisées sous forme de dictionnaires
        if isinstance(serializer.data, list) and isinstance(serializer.data[0], dict):
            for item in serializer.data:
                etat_obj = Etat.objects.filter(code_etat=item.get('code_etat')).first()

                if etat_obj:
                    item['libelle_etat'] = etat_obj.libelle
                else:
                    item['libelle_etat'] = "État introuvable"
        else:
            # Ajout du libellé de l'état à chaque objet sérialisé
            for item in serializer.data:
                etat_info = item.get('etat', {})
                if etat_info:
                    code_etat = etat_info.get('code_etat')
                    etat_obj = Etat.objects.filter(code_etat=code_etat).first()

                    if etat_obj:
                        etat_info['libelle'] = etat_obj.libelle
                    else:
                        etat_info['libelle'] = "État introuvable"

        return Response(serializer.data, status=status.HTTP_200_OK)
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import F
from .models import Colis, Expediteur, EtatColis

def colis_par_expediteur_et_etat(request, code_expediteur, code_etat):
    result = (
        Colis.objects
        .filter(
            expediteur__code_expediteur=code_expediteur,
            etatcolis__code_etat=code_etat,
        )
        .values(
            'code_colis',
            'nom_clt',
            'gouvernement',
            'ville',
            'adresse_clt',
            'tel_clt',
            'tel_clt2',
            'des',
            'prix',
            'nb_article',
            'date',
            'commentaire',
            'mode_paiement',
            'expediteur__nom_expediteur',  # Incluez les champs de l'expéditeur si nécessaire
        )
    )
    
    return JsonResponse(list(result), safe=False)
class TestView(View):
    def get(self, request):
        # Cette vue renvoie une chaîne simple
        return HttpResponse("Connexion réussie entre Django et Android!")