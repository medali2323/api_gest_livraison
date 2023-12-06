import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils import timezone


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	is_ens			        = models.BooleanField(default=False)
	is_adj         			= models.BooleanField(default=False)
	is_parent   			= models.BooleanField(default=False)


	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Expediteur(models.Model):
    code_expediteur = models.AutoField(primary_key=True)
    user = models.OneToOneField(Account, null=True, blank=True, on_delete=models.CASCADE)

    nom_expediteur = models.CharField(max_length=255)
    num_tel_expediteur = models.CharField(max_length=15)
    gouvernement = models.CharField(max_length=255)
    adresse = models.TextField()
    ville = models.CharField(max_length=255)
    code_tva = models.CharField(max_length=255)
    email = models.EmailField()
    mode_paiement = models.CharField(max_length=255)
    frais_livraison = models.FloatField()
    frais_retour = models.FloatField()

    def __str__(self):
        return self.nom_expediteur
class Colis(models.Model):
    code_colis = models.AutoField(primary_key=True)
    code_barre = models.CharField(max_length=12, unique=True, null=True, blank=True)

    nom_clt = models.CharField(max_length=255)
    gouvernement = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    adresse_clt = models.TextField()
    tel_clt = models.CharField(max_length=15)
    tel_clt2 = models.CharField(max_length=15, null=True, blank=True)
    des = models.CharField(max_length=255)
    prix = models.FloatField()
    nb_article = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    commentaire = models.TextField(max_length=15, null=True, blank=True)
    mode_paiement = models.CharField(max_length=255)
    expediteur = models.ForeignKey(Expediteur, on_delete=models.SET_NULL, null=True, blank=True)

        
    def __str__(self):
        return f"{self.nom_clt} - {self.code_colis}"

class Depot(models.Model):
    id_depot = models.AutoField(primary_key=True)
    user = models.OneToOneField(Account, null=True, blank=True, on_delete=models.CASCADE)

    ville = models.CharField(max_length=255)
    adresse = models.TextField()
    num_tel = models.CharField(max_length=15)

    def __str__(self):
        return self.ville
    
class Livreur(models.Model):
    code_livreur = models.AutoField(primary_key=True)
    user = models.OneToOneField(Account, null=True, blank=True, on_delete=models.CASCADE)

    nom_livreur = models.CharField(max_length=255)
    num_tel = models.CharField(max_length=15)
    frais_livraison = models.CharField(max_length=255)  # Assurez-vous que le type de données est approprié
    depot = models.ForeignKey(Depot, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nom_livreur

class Etat(models.Model):
    code_etat = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=255)

    def __str__(self):
        return self.libelle
class EtatColis(models.Model):
    code_etat_colis = models.AutoField(primary_key=True)
    code_colis = models.ForeignKey(Colis, on_delete=models.CASCADE)
    code_etat = models.ForeignKey(Etat, on_delete=models.CASCADE)
    code_livreur = models.ForeignKey(Livreur, on_delete=models.CASCADE,null=True, blank=True)
    date = models.DateTimeField()
    commentaire = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"EtatColis {self.code_etat_colis}"
    def get_libelle_etat(self, obj):
        return obj.code_etat.libelle

class Reclamation(models.Model):
    code_reclamation = models.AutoField(primary_key=True)
    type_reclamation = models.CharField(max_length=255)
    etat_reclamation = models.CharField(max_length=255)
    commentaire = models.TextField()
    date = models.DateField()
    code_colis = models.ForeignKey(Colis, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reclamation {self.code_reclamation}"
class RecetteExpediteur(models.Model):
    code_recette = models.AutoField(primary_key=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    montant_expediteur = models.FloatField()
    montant_societe = models.FloatField()
    nb_colis_livre = models.IntegerField()
    nb_colis_retour = models.IntegerField()
    code_expediteur = models.ForeignKey(Expediteur, on_delete=models.CASCADE)
