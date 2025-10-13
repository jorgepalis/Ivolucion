from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser,
	BaseUserManager,
	PermissionsMixin,
)


class Role(models.Model):
	"""modelo para roles de usuario (admin, client)"""
	name = models.CharField(max_length=50, unique=True)

	class Meta:
		verbose_name = 'Role'
		verbose_name_plural = 'Roles'

	def __str__(self):
		return self.name


class UserManager(BaseUserManager):
	"""Manager para el modelo User que utiliza email en lugar de username"""
	def _create_user(self, email, password, **extra_fields):
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

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	"""modelo de usuario"""
	email = models.EmailField(unique=True)
	name = models.CharField(max_length=150, blank=True)
	role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def __str__(self):
		return self.email
	
	@property
	def is_admin(self):
		return self.role and self.role.name == 'admin'
	
	@property
	def is_client(self):
		return self.role and self.role.name == 'client'
