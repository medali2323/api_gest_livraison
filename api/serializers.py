
# serializers.py

from rest_framework import serializers
from .models import Expediteur, Colis, Depot, Livreur, Etat, EtatColis, Reclamation, RecetteExpediteur,Account
class RegistrationSerializer(serializers.ModelSerializer):

	password2 				= serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = Account
		fields = ['email', 'username', 'password', 'password2']
		extra_kwargs = {
				'password': {'write_only': True},
		}	


	def	save(self):

		account = Account(
					email=self.validated_data['email'],
					username=self.validated_data['username']
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		account.set_password(password)
		account.save()
		return account
from .models import *



	




class ChangePasswordSerializer(serializers.Serializer):
    model = Account

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
class ExpediteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expediteur
        fields = '__all__'

class ColisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colis
        fields = '__all__'

class DepotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depot
        fields = '__all__'

class LivreurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livreur
        fields = '__all__'

class EtatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etat
        fields = '__all__'

class EtatColisSerializer(serializers.ModelSerializer):
    etat = EtatSerializer(source='code_etat', read_only=True)
    libelle_etat = serializers.SerializerMethodField()

    class Meta:
        model = EtatColis
        fields = '__all__'

    def get_libelle_etat(self, obj):
        return obj.code_etat.libelle
class ReclamationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reclamation
        fields = '__all__'

class RecetteExpediteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetteExpediteur
        fields = '__all__'
