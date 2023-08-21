from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .utils import *
from django.contrib.auth.models import AbstractUser, BaseUserManager
#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

# Create your models here.
class Client(models.Model):
	GENDER= (
		('MALE', 'MALE'),
		('FEMALE', 'FEMALE'),
		('TRANSGENDER', 'TRANSGENDER'),
		('RATHER NOT SAY', 'RATHER NOT SAY'),
		)
	KIN_GENDER= (
		('MALE', 'MALE'),
		('FEMALE', 'FEMALE'),
		('TRANSGENDER', 'TRANSGENDER'),
		('RATHER NOT SAY', 'RATHER NOT SAY'),
		)
	RELATIONSHIP=(
		('FATHER', 'FATHER'),
		('MOTHER', 'MOTHER'),
		('SIBLING', 'SIBLING'),
		('SPOUSE', 'SPOUSE'),
		('OTHERS', 'OTHERS'),
		)
	user= models.OneToOneField(CustomUser, on_delete= models.CASCADE)
	bio= models.TextField(blank= True)
	first_name= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	last_name= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	email_address= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	country= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	city= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	home_address= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	Date_of_birth= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	gender= models.CharField(max_length=64, default='update your account', null=True, blank=True, choices=GENDER)
	occupation= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	monthly_income= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	reason_for_investing= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	code= models.CharField(max_length=12, blank=True)
	recommended_by= models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
	updated= models.DateTimeField(auto_now= True)
	created= models.DateTimeField(auto_now_add= True)
	deposit= models.FloatField(default=0, null=True)
	balance= models.FloatField(default=0,null=True)
	withdrawal= models.FloatField(default=0,null=True)
	profit= models.FloatField(default=0,null=True)
	roi= models.FloatField(default=0.015, null=True)
	running_days= models.IntegerField(default=0, null=True)
	wallet_address= models.CharField(max_length=400, default='update your account', null=True)
	ID_CARD= models.ImageField(null=True, blank=True)
	next_of_kin_fullname= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	next_of_kin_phonenumber= models.CharField(max_length=64, default='update your account', null=True, blank=True)
	next_of_kin_gender= models.CharField(max_length=64, default='update your account', null=True, blank=True, choices=KIN_GENDER)
	next_of_kin_age= models.CharField(max_length=64, default='update your account', null=True, blank=True,)
	next_of_kin_phonenumber= models.CharField(max_length=64, default='update your account', null=True, blank=True,)
	next_of_kin_home_address= models.CharField(max_length=64, default='update your account', null=True, blank=True,)
	relationship_status_with_next_of_kin= models.CharField(max_length=64, default='update your account', null=True, blank=True, choices=RELATIONSHIP)

	def __str__(self):
		return f'{self.user.email}-{self.code}'

	@property
	def profile_picUrl(self):
		try:
			url= self.profile_pic.url
		except:
			url=''
		return url

	def get_recommended_profiles(self):
		query= Client.objects.all()
		my_recs= []
		for i in query:
			if i.recommended_by== self.user:
				my_recs.append(i)
		return my_recs


	def save(self, *args, **kwargs):
		if self.code=='':
			code= generate_ref_code()
			self.code= code
		super().save(*args, **kwargs)


class Payment_id(models.Model):
	client= models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
	payment_id= models.CharField(max_length=200, null=True)
	price_amount= models.CharField(max_length=200, null=True)
	investment_plan= models.FloatField(default=0.0052, null=True)
	date_created= models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return f'{self.client.user.email}'

class Plan(models.Model):
	investment_name= models.CharField(max_length=64, null=True, blank=True)
	mimimum_amount= models.FloatField(default=0, null=True, blank=True)
	maximum_amount= models.FloatField(default=0, null=True, blank=True)
	return_of_investment= models.CharField(max_length=5000, null=True, blank=True)
	duration= models.IntegerField(default=0, null=True, blank=True)

	def __str__(self):
		return self.investment_name

class Notification(models.Model):
	client= models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
	message_subject= models.CharField(max_length=200, blank=True, null=True)
	message_body= models.TextField(max_length=1500, blank=True, null=True)
	created= models.DateTimeField(auto_now_add= True)

	def __str__(self):
		return f'{ self.client.user.email} - {self.message_subject }'

class Withdrawal_request(models.Model):
	client= models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
	client_username= models.CharField(max_length=200, null=True)
	client_email= models.CharField(max_length=200, null=True)
	transaction_hash= models.CharField(max_length=20, null=True,)
	crypto_used_for_requesting_withdrawal= models.CharField(max_length=35, null=True)
	withdrawal_address= models.CharField(max_length=200, null=True)
	amount= models.FloatField(default=0, null=True)
	date_created= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.client_username

	def save(self, *args, **kwargs):
		if self.transaction_hash == "":
			transaction_hash= transaction_hash_code()
			self.transaction_hash = transaction_hash
		super().save(*args, **kwargs)

class Transaction(models.Model):
	client= models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
	transaction_type= models.CharField(max_length=64, null=True, blank=True)
	transaction_id= models.CharField(max_length=30, null=True, blank=True, default='504ID.omit')
	investment_plan= models.CharField(max_length=64, null=True, blank=True, default='504Package.omit')
	amount= models.FloatField(default=0, null=True)
	status= models.CharField(max_length=64, null=True, blank=True)
	created= models.DateTimeField(auto_now_add= True, null=True, blank=True)
	def __str__(self):
		return self.client.user.email

class Bonus(models.Model):
	client= models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
	transaction_type= models.CharField(max_length=64, null=True, blank=True, default='Pending Bonus')
	amount= models.FloatField(default=0, null=True)
	code= models.CharField(max_length=8, null=True, blank=True, unique=True)
	client_email= models.CharField(max_length=68, null=True, blank=True)
	message= models.TextField(max_length=1000, null=True, blank=True)
	created= models.DateTimeField(auto_now_add= True, null=True, blank=True)
	def __str__(self):
		return self.client.user.email

class Minimum_withdrawal(models.Model):
    minimum_withdrawal= models.FloatField(default=0)

    def __str__(self):
        return f"Your minimum withdrawal goes here"

class Maximum_withdrawal(models.Model):
    maximum_withdrawal= models.FloatField(default=0)

    def __str__(self):
        return f"Your maximum withdrawal goes here"

class Video(models.Model):
	meeting_agenda= models.CharField(max_length=68, null=True, blank=True, default="Live Video")
	video = models.FileField(null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
	date_uploaded = models.DateTimeField(auto_now_add= True)

	def __str__(self):
		return f" {self.meeting_agenda} - Only post one video at a time. Delete then post another one."